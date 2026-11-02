#!/usr/bin/env python3
"""List / download files of a public Zenodo record, verifying Zenodo's checksum.

Standard library + system curl. Idempotent (size + checksum match -> skip).
--dry-run writes the manifest only.

Usage:
    python3 zenodo_download.py 7961605 --out data/raw/zenodo_7961605 --dry-run
    python3 zenodo_download.py 7961605 --out data/raw/zenodo_7961605
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone


def get_record(rid):
    url = f"https://zenodo.org/api/records/{rid}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"  Zenodo API failed ({attempt + 1}/4): {exc}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    sys.exit(f"cannot read Zenodo record {rid}")


def digest(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(16 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("record")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rec = get_record(args.record)
    meta = rec.get("metadata", {})
    print(f"record {args.record}: {meta.get('title')}")
    print(f"doi: {rec.get('doi')}  license: {(meta.get('license') or {}).get('id')}  "
          f"published: {meta.get('publication_date')}")
    files = []
    for f in rec.get("files", []):
        algo, _, value = (f.get("checksum") or ":").partition(":")
        link = f.get("links", {}).get("self") or f.get("links", {}).get("content")
        files.append({"name": f.get("key"), "size": int(f.get("size", -1)), "algo": algo,
                      "checksum": value, "url": link})
    total = sum(f["size"] for f in files if f["size"] > 0)
    print(f"{len(files)} files, {total / 1e9:.2f} GB")
    for f in files:
        print(f"  {f['size'] / 1e9:8.2f} GB  {f['name']}  [{f['algo']}]")

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "zenodo_manifest.tsv"), "w", encoding="utf-8") as fh:
        fh.write("file\tsize_bytes\tchecksum_algo\tchecksum\turl\n")
        for f in files:
            fh.write(f"{f['name']}\t{f['size']}\t{f['algo']}\t{f['checksum']}\t{f['url']}\n")
    if args.dry_run:
        return

    prov = os.path.join(args.out, "provenance.tsv")
    if not os.path.exists(prov):
        with open(prov, "w", encoding="utf-8") as fh:
            fh.write("date_utc\tfile\turl\tsize_bytes\tchecksum_expected\tchecksum_observed\tstatus\n")
    for f in files:
        dest = os.path.join(args.out, f["name"])
        status, observed = None, ""
        if os.path.exists(dest) and os.path.getsize(dest) == f["size"]:
            observed = digest(dest, f["algo"] or "md5")
            status = "cached" if observed == f["checksum"] else None
        if status is None:
            for attempt in range(4):
                if os.path.exists(dest) and os.path.getsize(dest) > f["size"]:
                    os.remove(dest)
                rc = subprocess.call(["curl", "-sS", "-L", "--fail", "--retry", "8", "--retry-delay", "15",
                                      "--retry-all-errors", "-C", "-", "-o", dest, f["url"]])
                if rc == 0 and os.path.exists(dest) and os.path.getsize(dest) == f["size"]:
                    observed = digest(dest, f["algo"] or "md5")
                    if observed == f["checksum"]:
                        status = "downloaded"
                        break
                    os.remove(dest)
                time.sleep(15 * (attempt + 1))
            status = status or "FAILED"
        print(f"[{status}] {f['name']}", flush=True)
        with open(prov, "a", encoding="utf-8") as fh:
            fh.write("\t".join([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), f["name"], f["url"] or "",
                                str(f["size"]), f["checksum"], observed, status]) + "\n")


if __name__ == "__main__":
    main()
