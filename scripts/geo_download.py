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
from datetime import datetime, timezone

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


def _open_soft(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "rt", encoding="utf-8", errors="replace")


def _soft_is_valid(path):
    """A usable SOFT file is non-empty, decompresses, and declares the series."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False
    try:
        with _open_soft(path) as fh:
            head = fh.read(200000)
        return "^SERIES" in head
    except Exception:  # noqa: BLE001
        return False


def fetch_soft(acc, cache):
    """Return a path to a valid SOFT file for acc, or None.

    GEO's FTP mirror sometimes answers 200 with an empty body, so every fetch is
    validated. After the FTP copy fails, fall back to the acc.cgi text export
    (same records, brief view, uncompressed)."""
    os.makedirs(cache, exist_ok=True)
    ftp_dest = os.path.join(cache, f"{acc}_family.soft.gz")
    cgi_dest = os.path.join(cache, f"{acc}_family.soft")
    for path in (ftp_dest, cgi_dest):
        if _soft_is_valid(path):
            return path
    sources = [
        (f"{GEO_FTP}/{series_dir(acc)}/{acc}/soft/{acc}_family.soft.gz", ftp_dest),
        (f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={acc}&targ=all&form=text&view=brief", cgi_dest),
    ]
    for url, dest in sources:
        for attempt in range(4):
            try:
                _download_with_ua(url, dest)
            except Exception as exc:  # noqa: BLE001
                print(f"  soft fetch error ({attempt + 1}/4) {url}: {exc}", file=sys.stderr)
            if _soft_is_valid(dest):
                return dest
            size = os.path.getsize(dest) if os.path.exists(dest) else -1
            print(f"  soft fetch gave unusable file ({attempt + 1}/4, {size} bytes): {url}", file=sys.stderr)
            if os.path.exists(dest):
                os.remove(dest)
            time.sleep(5 * (attempt + 1))
    return None


def supplementary_urls(soft_path):
    """Yield (gsm_or_series, url) for every supplementary file in a SOFT family file."""
    current = None
    with _open_soft(soft_path) as fh:
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
    """Content-Length in bytes, or -1 if the server never answered. GEO drops some
    HEAD requests under load, so retry with backoff."""
    req = urllib.request.Request(url, method="HEAD", headers=UA)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                length = resp.headers.get("Content-Length")
                return int(length) if length is not None else -1
        except Exception:  # noqa: BLE001
            time.sleep(2 * (attempt + 1))
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
    if expected_size < 0:
        expected_size = head_size(url)  # second chance after the bulk HEAD pass
    if expected_size > 0 and os.path.exists(dest) and os.path.getsize(dest) == expected_size:
        return "cached", dest, expected_size, None
    cmd = ["curl", "-sS", "-L", "-A", "Mozilla/5.0", "--retry", "8", "--retry-delay", "10", "--retry-all-errors",
           "-C", "-", "-o", dest, url]
    for attempt in range(3):
        rc = subprocess.call(cmd)
        size = os.path.getsize(dest) if os.path.exists(dest) else 0
        if rc == 0 and expected_size >= 0 and size == expected_size:
            return "downloaded", dest, size, sha256_of(dest)
        if rc == 0 and expected_size < 0:
            return "downloaded_size_unverified", dest, size, sha256_of(dest)
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

        print(f"   SOFT: {soft}")
        if not items:
            print(f"   WARNING: {acc} has no supplementary files in its SOFT record "
                  f"(data may be SRA/dbGaP only, or the series is not public)", file=sys.stderr)
        print(f"   {len(items)} files selected; fetching sizes")
        sizes = {}
        with ThreadPoolExecutor(max_workers=4) as ex:
            futs = {ex.submit(head_size, url): url for _, url in items}
            for f in as_completed(futs):
                sizes[futs[f]] = f.result()
        total = sum(s for s in sizes.values() if s > 0)
        grand_total += total
        print(f"   total {total / 1e9:.2f} GB")
        for gsm, url in items:
            s = sizes.get(url, -1)
            size_txt = f"{s / 1e9:9.3f} GB" if s >= 0 else "  unknown   "
            print(f"   {size_txt}  {gsm}  {os.path.basename(url)}")
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
                    fh.write("\t".join([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), acc, gsm,
                                        os.path.basename(dest), url, str(size), digest or "",
                                        status]) + "\n")
    print(f"== grand total selected: {grand_total / 1e9:.2f} GB")


if __name__ == "__main__":
    main()
