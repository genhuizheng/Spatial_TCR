#!/usr/bin/env python3
"""Phase A audit: pull GEO SOFT metadata for a list of series and tabulate
samples and supplementary files (with sizes) WITHOUT downloading data.

Standard library only, so it runs on a TACC login node with system python3.

Usage:
    python3 geo_audit.py --out metadata --cache data/raw/geo_meta GSE300147 GSE287301

Outputs (in --out):
    geo_series_summary.txt   human-readable per-series summary
    geo_samples.tsv          one row per GSM
    geo_files.tsv            one row per supplementary file, with size
    geo_file_urls.txt        plain URL list for later selective download
"""
import argparse
import gzip
import os
import sys
import time
import urllib.request
import urllib.error
from collections import OrderedDict

GEO_FTP = "https://ftp.ncbi.nlm.nih.gov/geo/series"
UA = {"User-Agent": "Mozilla/5.0 (spatial_TCR download scripts; contact via GEO)"}


def _download_with_ua(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)


def series_dir(acc):
    # GSE300147 -> GSE300nnn ; GSE238071 -> GSE238nnn
    return acc[:-3] + "nnn"


def fetch(url, dest, retries=3):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    for attempt in range(retries):
        try:
            _download_with_ua(url, dest)
            return dest
        except Exception as exc:  # noqa: BLE001
            print(f"  fetch failed ({attempt + 1}/{retries}): {url} -> {exc}", file=sys.stderr)
            time.sleep(3)
    return None


def head_size(url, retries=2):
    """Return Content-Length in bytes or -1. ftp:// URLs are rewritten to https."""
    if url.startswith("ftp://ftp.ncbi.nlm.nih.gov"):
        url = "https://" + url[len("ftp://"):]
    req = urllib.request.Request(url, method="HEAD", headers=UA)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                length = resp.headers.get("Content-Length")
                return int(length) if length is not None else -1
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return -404
            time.sleep(2)
        except Exception:  # noqa: BLE001
            time.sleep(2)
    return -1


def parse_soft(path):
    """Minimal SOFT family parser. Returns (series_dict, [sample_dict])."""
    series = OrderedDict()
    samples = []
    current = None
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("^SERIES"):
                current = series
                series["accession"] = line.split("=", 1)[1].strip()
                continue
            if line.startswith("^SAMPLE"):
                current = OrderedDict()
                current["accession"] = line.split("=", 1)[1].strip()
                samples.append(current)
                continue
            if line.startswith("^PLATFORM") or line.startswith("^DATABASE"):
                current = None
                continue
            if current is None or not line.startswith("!"):
                continue
            if "=" not in line:
                continue
            key, val = line[1:].split("=", 1)
            key = key.strip()
            val = val.strip()
            # strip the Series_/Sample_ prefix for compactness
            for prefix in ("Series_", "Sample_"):
                if key.startswith(prefix):
                    key = key[len(prefix):]
            current.setdefault(key, []).append(val)
    return series, samples


def first(d, key, default=""):
    v = d.get(key)
    return v[0] if v else default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accessions", nargs="+")
    ap.add_argument("--out", default="metadata")
    ap.add_argument("--cache", default="data/raw/geo_meta")
    ap.add_argument("--no-sizes", action="store_true", help="skip HEAD requests for file sizes")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.cache, exist_ok=True)

    summary_lines = []
    sample_rows = []
    file_rows = []
    urls = []

    for acc in args.accessions:
        print(f"== {acc}")
        soft_url = f"{GEO_FTP}/{series_dir(acc)}/{acc}/soft/{acc}_family.soft.gz"
        soft_path = os.path.join(args.cache, f"{acc}_family.soft.gz")
        if fetch(soft_url, soft_path) is None:
            summary_lines.append(f"### {acc}\nFAILED to fetch {soft_url}\n")
            continue

        series, samples = parse_soft(soft_path)
        title = first(series, "title")
        summary_lines.append(f"### {acc}  {title}")
        summary_lines.append(f"status: {first(series, 'status')}  |  samples: {len(samples)}  |  platform(s): {', '.join(series.get('platform_id', []))}")
        summary_lines.append(f"type: {', '.join(series.get('type', []))}")
        summary_lines.append("summary: " + " ".join(series.get("summary", []))[:1500])
        summary_lines.append("overall_design: " + " ".join(series.get("overall_design", []))[:1500])
        for rel in series.get("relation", []):
            summary_lines.append(f"relation: {rel}")
        summary_lines.append("")

        # series-level supplementary files
        for url in series.get("supplementary_file", []):
            if url and url.upper() != "NONE":
                file_rows.append([acc, acc, "series", os.path.basename(url), url])
                urls.append(url)

        for s in samples:
            gsm = s["accession"]
            chars = "; ".join(s.get("characteristics_ch1", []))
            sample_rows.append([
                acc, gsm,
                first(s, "title"),
                first(s, "organism_ch1"),
                first(s, "source_name_ch1"),
                first(s, "library_strategy"),
                first(s, "library_source"),
                first(s, "instrument_model"),
                chars,
                " | ".join(s.get("relation", [])),
            ])
            for key in sorted(k for k in s if k.startswith("supplementary_file")):
                for url in s[key]:
                    if url and url.upper() != "NONE":
                        file_rows.append([acc, gsm, first(s, "title"), os.path.basename(url), url])
                        urls.append(url)

        n_files = sum(1 for r in file_rows if r[0] == acc)
        print(f"   samples={len(samples)} supplementary_files={n_files}")

    # sizes
    total_by_series = {}
    if not args.no_sizes:
        print(f"== HEAD requests for {len(file_rows)} files")
        for i, row in enumerate(file_rows, 1):
            size = head_size(row[4])
            row.append(str(size))
            row.append(f"{size / 1e9:.3f}" if size > 0 else "NA")
            if size > 0:
                total_by_series[row[0]] = total_by_series.get(row[0], 0) + size
            if i % 20 == 0:
                print(f"   {i}/{len(file_rows)}")
    else:
        for row in file_rows:
            row.extend(["NA", "NA"])

    summary_lines.append("### Supplementary file totals (bytes reported by server)")
    for acc in args.accessions:
        tot = total_by_series.get(acc, 0)
        n = sum(1 for r in file_rows if r[0] == acc)
        summary_lines.append(f"{acc}: {n} files, {tot / 1e9:.2f} GB")

    with open(os.path.join(args.out, "geo_series_summary.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(summary_lines) + "\n")

    with open(os.path.join(args.out, "geo_samples.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\t".join(["series", "gsm", "title", "organism", "source_name", "library_strategy",
                            "library_source", "instrument", "characteristics", "relations"]) + "\n")
        for r in sample_rows:
            fh.write("\t".join(x.replace("\t", " ") for x in r) + "\n")

    with open(os.path.join(args.out, "geo_files.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\t".join(["series", "gsm", "sample_title", "filename", "url", "size_bytes", "size_gb"]) + "\n")
        for r in file_rows:
            fh.write("\t".join(x.replace("\t", " ") for x in r) + "\n")

    with open(os.path.join(args.out, "geo_file_urls.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(urls) + "\n")

    print("\n".join(summary_lines[-(len(args.accessions) + 1):]))
    print(f"wrote {args.out}/geo_series_summary.txt, geo_samples.tsv, geo_files.tsv, geo_file_urls.txt")


if __name__ == "__main__":
    main()
