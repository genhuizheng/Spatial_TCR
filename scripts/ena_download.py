#!/usr/bin/env python3
"""Download raw FASTQ runs for an ENA/SRA study or run list, verifying ENA's MD5.

Standard library + system curl. Idempotent: a file whose size and MD5 already
match ENA is skipped. Separate manifest step (--dry-run) from download.

Usage:
    python3 ena_download.py --out data/raw/PRJNA742564 --dry-run PRJNA742564
    python3 ena_download.py --out data/raw/PRJNA742564 PRJNA742564
Layout:  <out>/<run>/<file>.fastq.gz ; manifest <out>/ena_manifest.tsv ;
         provenance appended to <out>/provenance.tsv
"""
import argparse
import hashlib
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

FIELDS = ["run_accession", "sample_accession", "sample_title", "library_strategy", "library_source",
          "read_count", "base_count", "fastq_bytes", "fastq_md5", "fastq_ftp"]


def ena_runs(accession):
    q = urllib.parse.urlencode({"accession": accession, "result": "read_run",
                                "fields": ",".join(FIELDS), "format": "tsv"})
    url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?{q}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                lines = r.read().decode("utf-8").strip().split("\n")
            header = lines[0].split("\t")
            return [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln.strip()]
        except Exception as exc:  # noqa: BLE001
            print(f"  ENA query failed ({attempt + 1}/4): {exc}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    sys.exit(f"cannot query ENA for {accession}")


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(16 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accessions", nargs="+", help="study / project / run accessions")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = []
    for acc in args.accessions:
        for run in ena_runs(acc):
            urls = [u for u in run.get("fastq_ftp", "").split(";") if u]
            sizes = run.get("fastq_bytes", "").split(";")
            md5s = run.get("fastq_md5", "").split(";")
            if not urls:
                print(f"  WARNING {run['run_accession']}: no FASTQ listed by ENA", file=sys.stderr)
            for u, s, m in zip(urls, sizes, md5s):
                files.append({"run": run["run_accession"], "sample": run.get("sample_accession", ""),
                              "title": run.get("sample_title", ""), "url": "https://" + u,
                              "size": int(s) if s else -1, "md5": m, "name": os.path.basename(u)})

    total = sum(f["size"] for f in files if f["size"] > 0)
    print(f"{len(files)} FASTQ files, {total / 1e9:.2f} GB")
    for f in files:
        print(f"  {f['size'] / 1e6:9.1f} MB  {f['run']}  {f['title']:<20}  {f['name']}")

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "ena_manifest.tsv"), "w", encoding="utf-8") as fh:
        fh.write("run\tsample\tsample_title\tfile\tsize_bytes\tmd5\turl\n")
        for f in files:
            fh.write(f"{f['run']}\t{f['sample']}\t{f['title']}\t{f['name']}\t{f['size']}\t{f['md5']}\t{f['url']}\n")
    if args.dry_run:
        print(f"manifest written: {os.path.join(args.out, 'ena_manifest.tsv')} (dry run, nothing downloaded)")
        return

    prov = os.path.join(args.out, "provenance.tsv")
    if not os.path.exists(prov):
        with open(prov, "w", encoding="utf-8") as fh:
            fh.write("date_utc\trun\tfile\turl\tsize_bytes\tmd5_expected\tmd5_observed\tstatus\n")
    n_bad = 0
    for f in files:
        dest_dir = os.path.join(args.out, f["run"])
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, f["name"])
        status, observed = None, ""
        if os.path.exists(dest) and os.path.getsize(dest) == f["size"]:
            observed = md5_of(dest)
            if observed == f["md5"]:
                status = "cached"
        if status is None:
            for attempt in range(4):
                if os.path.exists(dest) and os.path.getsize(dest) > f["size"]:
                    os.remove(dest)
                rc = subprocess.call(["curl", "-sS", "-L", "--fail", "--retry", "8", "--retry-delay", "10",
                                      "--retry-all-errors", "-C", "-", "-o", dest, f["url"]])
                size = os.path.getsize(dest) if os.path.exists(dest) else 0
                if rc == 0 and size == f["size"]:
                    observed = md5_of(dest)
                    if observed == f["md5"]:
                        status = "downloaded"
                        break
                    os.remove(dest)  # right size, wrong content: start over
                time.sleep(10 * (attempt + 1))
            if status is None:
                status = "FAILED"
                n_bad += 1
        print(f"[{status}] {f['run']}/{f['name']}", flush=True)
        with open(prov, "a", encoding="utf-8") as fh:
            fh.write("\t".join([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), f["run"], f["name"],
                                f["url"], str(f["size"]), f["md5"], observed, status]) + "\n")
    print(f"done: {len(files) - n_bad}/{len(files)} files verified by MD5")


if __name__ == "__main__":
    main()
