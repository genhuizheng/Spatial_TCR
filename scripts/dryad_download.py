#!/usr/bin/env python3
"""List and download the files of a Dryad dataset through the Dryad v2 API,
with resume, size check and digest verification.

Standard library + system curl.

Listing files needs no credentials. Downloading does (Dryad answers 401
"must have current bearer token" otherwise). Provide either
    DRYAD_CLIENT_ID + DRYAD_CLIENT_SECRET  (API account from https://datadryad.org/account;
                                            the script exchanges them for a 10-hour token)
or  DRYAD_TOKEN                            (a bearer token copied from the account page)
as environment variables. They are never put on a command line, so other
users on a shared login node cannot see them in `ps`.

Usage:
    python3 dryad_download.py --out data/raw/dryad_h70rxwdmj --dry-run 10.5061/dryad.h70rxwdmj
    python3 dryad_download.py --out data/raw/dryad_h70rxwdmj --exclude 'MALDI|Methylation' 10.5061/dryad.h70rxwdmj
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://datadryad.org"


def get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"  API call failed ({attempt + 1}/3): {url} -> {exc}", file=sys.stderr)
            time.sleep(3)
    return None


def list_files(doi):
    ds = get_json(f"{API}/api/v2/datasets/{urllib.parse.quote('doi:' + doi, safe='')}")
    if ds is None:
        sys.exit("dataset lookup failed")
    title = ds.get("title")
    version_link = ds["_links"]["stash:version"]["href"]
    print(f"dataset: {title}")
    print(f"version: {version_link}  (versionNumber {ds.get('versionNumber')})")
    files = []
    page = 1
    while True:
        js = get_json(f"{API}{version_link}/files?page={page}&per_page=100")
        if js is None:
            break
        batch = js.get("_embedded", {}).get("stash:files", [])
        for f in batch:
            dl = f["_links"].get("stash:download", {}).get("href")
            files.append({
                "path": f.get("path"),
                "size": int(f.get("size", -1)),
                "digest": f.get("digest"),
                "digest_type": f.get("digestType"),
                "mime": f.get("mimeType"),
                "download": f"{API}{dl}" if dl else None,
            })
        if "next" in js.get("_links", {}):
            page += 1
        else:
            break
    return files


def get_token():
    """Bearer token from DRYAD_TOKEN, or exchanged from DRYAD_CLIENT_ID/SECRET."""
    token = os.environ.get("DRYAD_TOKEN", "").strip()
    if token:
        return token
    cid = os.environ.get("DRYAD_CLIENT_ID", "").strip()
    secret = os.environ.get("DRYAD_CLIENT_SECRET", "").strip()
    if not (cid and secret):
        return None
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": secret,
                                   "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(f"{API}/oauth/token", data=body, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            js = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"token request failed: {exc}")
    token = js.get("access_token")
    if not token:
        sys.exit(f"token response had no access_token: {sorted(js)}")
    hours = (js.get("expires_in") or 0) / 3600
    print(f"obtained bearer token (valid {hours:.1f} h)")
    return token


def curl_download(url, dest, token):
    """curl with resume. The Authorization header goes in through stdin (-K -),
    so the token never appears in the process list. --fail keeps HTTP error
    bodies out of the output file."""
    cfg = f'header = "Authorization: Bearer {token}"\n'
    cmd = ["curl", "-sS", "-L", "--fail", "-A", "Mozilla/5.0", "--retry", "8", "--retry-delay", "10",
           "--retry-all-errors", "-C", "-", "-K", "-", "-o", dest, url]
    return subprocess.run(cmd, input=cfg, text=True).returncode


def digest_of(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(16 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doi", help="e.g. 10.5061/dryad.h70rxwdmj")
    ap.add_argument("--out", required=True)
    ap.add_argument("--include", default=None)
    ap.add_argument("--exclude", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    inc = re.compile(args.include) if args.include else None
    exc = re.compile(args.exclude) if args.exclude else None

    files = list_files(args.doi)
    selected = [f for f in files
                if (not inc or inc.search(f["path"])) and (not exc or not exc.search(f["path"]))]
    total = sum(f["size"] for f in selected if f["size"] > 0)
    print(f"{len(files)} files in dataset, {len(selected)} selected, {total / 1e9:.2f} GB")
    for f in selected:
        print(f"  {f['size'] / 1e9:9.3f} GB  {f['path']}  [{f['digest_type']}]")
    if args.dry_run:
        return

    token = get_token()
    if not token:
        sys.exit("no credentials: export DRYAD_CLIENT_ID and DRYAD_CLIENT_SECRET (or DRYAD_TOKEN) first")

    os.makedirs(args.out, exist_ok=True)
    prov = os.path.join(args.out, "provenance.tsv")
    if not os.path.exists(prov):
        with open(prov, "w", encoding="utf-8") as fh:
            fh.write("date_utc\tpath\turl\tsize_bytes\tdigest_type\tdigest_expected\tdigest_observed\tstatus\n")

    for f in selected:
        dest = os.path.join(args.out, f["path"])
        if os.path.exists(dest) and os.path.getsize(dest) == f["size"]:
            status = "cached"
        else:
            # A small leftover that is not the real file is an old error body
            # (e.g. the 56-byte 401 JSON); resuming onto it would corrupt the file.
            if os.path.exists(dest):
                have = os.path.getsize(dest)
                if have > f["size"] or (have <= 4096 and have != f["size"]):
                    os.remove(dest)
            rc = curl_download(f["download"], dest, token)
            size = os.path.getsize(dest) if os.path.exists(dest) else 0
            status = "downloaded" if (rc == 0 and size == f["size"]) else f"FAILED(rc={rc},size={size})"
            if rc == 22 and size == 0:
                print("  HTTP error from Dryad (rc=22): token rejected or expired?", file=sys.stderr)
        observed = ""
        if status in ("downloaded", "cached") and f["digest"] and f["digest_type"]:
            algo = f["digest_type"].replace("-", "").lower()
            try:
                observed = digest_of(dest, algo)
                if observed != f["digest"]:
                    status = "DIGEST_MISMATCH"
            except ValueError:
                observed = "unsupported_algo"
        print(f"[{status}] {f['path']}", flush=True)
        with open(prov, "a", encoding="utf-8") as fh:
            fh.write("\t".join([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), f["path"], f["download"],
                                str(f["size"]), f["digest_type"] or "", f["digest"] or "", observed, status]) + "\n")


if __name__ == "__main__":
    main()
