#!/usr/bin/env python3
"""Download GEO supplementary files for one or more series, with resume,
size verification, SHA256 and a provenance table.

Standard library + system curl. Intended for a TACC login node under nohup
(downloads are pure network I/O).

Usage:
    python3 geo_download.py --out data/raw --exclude 'morphology' GSE300147
    python3 geo_download.py --out data/raw --dry-run GSE287301 GSE285951

Layout:  <out>/<ACCESSION>/<filename>
Provenance appended to <out>/provenance.tsv
"""
import argparse
import gzip
import hashlib
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

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
    return acc[:-3] + "nnn"


def to_https(url):
    if url.startswith("ftp://ftp.ncbi.nlm.nih.gov"):
        return "https://" + url[len("ftp://"):]
    return url


def fetch_soft(acc, cache):
    os.makedirs(cache, exist_ok=True)
    dest = os.path.join(cache, f"{acc}_family.soft.gz")
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    url = f"{GEO_FTP}/{series_dir(acc)}/{acc}/soft/{acc}_family.soft.gz"
    for attempt in range(3):
        try:
            _download_with_ua(url, dest)
            return dest
        except Exception as exc:  # noqa: BLE001
            print(f"  soft fetch failed ({attempt + 1}/3): {exc}", file=sys.stderr)
            time.sleep(3)
    return None


def supplementary_urls(soft_path):
    """Yield (gsm_or_series, url) for every supplementary file in a SOFT family file."""
    current = None
    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("^SERIES"):
                current = line.split("=", 1)[1].strip()
            elif line.startswith("^SAMPLE"):
                current = line.split("=", 1)[1].strip()
            elif line.startswith("^PLATFORM") or line.startswith("^DATABASE"):
                current = None
            elif current and ("_supplementary_file" in line) and "=" in line:
                url = line.split("=", 1)[1].strip()
                if url and url.upper() != "NONE":
                    yield current, to_https(url)


def head_size(url):
    req = urllib.request.Request(url, method="HEAD", headers=UA)
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                length = resp.headers.get("Content-Length")
                return int(length) if length is not None else -1
        except Exception:  # noqa: BLE001
            time.sleep(2)
    return -1


def sha256_of(path, bufsize=16 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(bufsize)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def download_one(item, out_dir, expected_size):
    """Download with curl resume. Returns (status, local_path, size, sha256)."""
    gsm, url = item
    fname = os.path.basename(url)
    dest = os.path.join(out_dir, fname)
    if expected_size > 0 and os.path.exists(dest) and os.path.getsize(dest) == expected_size:
        return "cached", dest, expected_size, None
    cmd = ["curl", "-sS", "-L", "-A", "Mozilla/5.0", "--retry", "8", "--retry-delay", "10", "--retry-all-errors",
           "-C", "-", "-o", dest, url]
    for attempt in range(3):
        rc = subprocess.call(cmd)
        size = os.path.getsize(dest) if os.path.exists(dest) else 0
        if rc == 0 and (expected_size <= 0 or size == expected_size):
            return "downloaded", dest, size, sha256_of(dest)
        if rc == 0 and expected_size > 0 and size > expected_size:
            # resume on a changed/corrupt partial file: start over
            os.remove(dest)
        time.sleep(5)
    size = os.path.getsize(dest) if os.path.exists(dest) else 0
    return f"FAILED(rc={rc},size={size},expected={expected_size})", dest, size, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accessions", nargs="+")
    ap.add_argument("--out", default="data/raw", help="root output directory")
    ap.add_argument("--cache", default="data/raw/geo_meta", help="where SOFT files are cached")
    ap.add_argument("--include", default=None, help="regex; only download files whose name matches")
    ap.add_argument("--exclude", default=None, help="regex; skip files whose name matches")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true", help="list and size files, download nothing")
    args = ap.parse_args()

    inc = re.compile(args.include) if args.include else None
    exc = re.compile(args.exclude) if args.exclude else None
    os.makedirs(args.out, exist_ok=True)
    prov_path = os.path.join(args.out, "provenance.tsv")
    if not os.path.exists(prov_path):
        with open(prov_path, "w", encoding="utf-8") as fh:
            fh.write("\t".join(["date_utc", "series", "gsm", "filename", "url", "size_bytes",
                                "sha256", "status"]) + "\n")

    grand_total = 0
    for acc in args.accessions:
        print(f"== {acc}")
        soft = fetch_soft(acc, args.cache)
        if soft is None:
            print(f"   could not fetch SOFT for {acc}; skipping", file=sys.stderr)
            continue
        items = []
        for gsm, url in supplementary_urls(soft):
            name = os.path.basename(url)
            if inc and not inc.search(name):
                continue
            if exc and exc.search(name):
                continue
            items.append((gsm, url))
        # de-duplicate (series-level and sample-level can repeat)
        seen = set()
        items = [it for it in items if not (it[1] in seen or seen.add(it[1]))]

        print(f"   {len(items)} files selected; fetching sizes")
        sizes = {}
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(head_size, url): url for _, url in items}
            for f in as_completed(futs):
                sizes[futs[f]] = f.result()
        total = sum(s for s in sizes.values() if s > 0)
        grand_total += total
        print(f"   total {total / 1e9:.2f} GB")
        for gsm, url in items:
            s = sizes.get(url, -1)
            print(f"   {s / 1e9:9.3f} GB  {gsm}  {os.path.basename(url)}")
        if args.dry_run:
            continue

        out_dir = os.path.join(args.out, acc)
        os.makedirs(out_dir, exist_ok=True)
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(download_one, it, out_dir, sizes.get(it[1], -1)): it for it in items}
            for f in as_completed(futs):
                gsm, url = futs[f]
                status, dest, size, digest = f.result()
                print(f"   [{status}] {os.path.basename(dest)} {size / 1e9:.3f} GB", flush=True)
                with open(prov_path, "a", encoding="utf-8") as fh:
                    fh.write("\t".join([datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), acc, gsm,
                                        os.path.basename(dest), url, str(size), digest or "",
                                        status]) + "\n")
    print(f"== grand total selected: {grand_total / 1e9:.2f} GB")


if __name__ == "__main__":
    main()
