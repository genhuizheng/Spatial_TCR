#!/usr/bin/env python3
"""List and download every file of an OSF project (osfstorage), recursively,
through the OSF v2 API. Works with view-only links by passing --view-only.

Standard library + system curl.

Usage:
    python3 osf_download.py 8qbdz --view-only 5287d7f6263e4ba680ca8c396aeefeee --out data/raw/osf_8qbdz --dry-run
    python3 osf_download.py 65y3t --view-only 6571f0c374ce4bf294b9cbd10ade62cf --out data/raw/osf_65y3t
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

API = "https://api.osf.io/v2"


def get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.api+json",
                                               "User-Agent": "Mozilla/5.0 (osf_download.py)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"  API call failed ({attempt + 1}/3): {url} -> {exc}", file=sys.stderr)
            time.sleep(3)
    return None


def with_view_only(url, token):
    if not token:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}view_only={token}"


def walk(url, token, prefix=""):
    """Yield file dicts (path, size, hashes, download) for a folder listing URL."""
    url = with_view_only(url, token)
    if "page%5Bsize%5D" not in url and "page[size]" not in url:
        url += "&page%5Bsize%5D=100"
    while url:
        js = get_json(url)
        if js is None:
            return
        for item in js.get("data", []):
            attrs = item.get("attributes", {})
            name = attrs.get("name")
            path = f"{prefix}{name}"
            if attrs.get("kind") == "folder":
                sub = item["relationships"]["files"]["links"]["related"]["href"]
                yield from walk(sub, token, prefix=path + "/")
            else:
                hashes = attrs.get("extra", {}).get("hashes", {})
                yield {
                    "path": path,
                    "size": int(attrs.get("size") or -1),
                    "sha256": hashes.get("sha256"),
                    "md5": hashes.get("md5"),
                    "download": item.get("links", {}).get("download"),
                }
        url = js.get("links", {}).get("next")
        if url:
            url = with_view_only(url, token)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(16 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("node", help="OSF node id, e.g. 8qbdz")
    ap.add_argument("--view-only", default=None, help="view_only token from a view-only link")
    ap.add_argument("--out", required=True)
    ap.add_argument("--include", default=None)
    ap.add_argument("--exclude", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    node = get_json(with_view_only(f"{API}/nodes/{args.node}/", args.view_only))
    if node is None or "data" not in node:
        sys.exit(f"cannot read node {args.node}: {node}")
    print(f"node {args.node}: {node['data']['attributes'].get('title')}")

    files = list(walk(f"{API}/nodes/{args.node}/files/osfstorage/", args.view_only))
    inc = re.compile(args.include) if args.include else None
    exc = re.compile(args.exclude) if args.exclude else None
    selected = [f for f in files
                if (not inc or inc.search(f["path"])) and (not exc or not exc.search(f["path"]))]
    total = sum(f["size"] for f in selected if f["size"] > 0)
    print(f"{len(files)} files, {len(selected)} selected, {total / 1e9:.3f} GB")
    for f in selected:
        print(f"  {f['size'] / 1e6:10.2f} MB  {f['path']}")
    if args.dry_run:
        return

    os.makedirs(args.out, exist_ok=True)
    prov = os.path.join(args.out, "provenance.tsv")
    if not os.path.exists(prov):
        with open(prov, "w", encoding="utf-8") as fh:
            fh.write("date_utc\tpath\turl\tsize_bytes\tsha256_expected\tsha256_observed\tstatus\n")
    for f in selected:
        dest = os.path.join(args.out, f["path"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        url = with_view_only(f["download"], args.view_only)
        if os.path.exists(dest) and os.path.getsize(dest) == f["size"]:
            status = "cached"
        else:
            cmd = ["curl", "-sS", "-L", "-A", "Mozilla/5.0", "--retry", "8", "--retry-delay", "10",
                   "--retry-all-errors", "-C", "-", "-o", dest, url]
            rc = subprocess.call(cmd)
            size = os.path.getsize(dest) if os.path.exists(dest) else 0
            status = "downloaded" if (rc == 0 and size == f["size"]) else f"FAILED(rc={rc},size={size})"
        observed = ""
        if status in ("downloaded", "cached") and f["sha256"]:
            observed = sha256_of(dest)
            if observed != f["sha256"]:
                status = "DIGEST_MISMATCH"
        print(f"[{status}] {f['path']}", flush=True)
        with open(prov, "a", encoding="utf-8") as fh:
            fh.write("\t".join([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), f["path"],
                                f["download"] or "", str(f["size"]), f["sha256"] or "", observed, status]) + "\n")


if __name__ == "__main__":
    main()
