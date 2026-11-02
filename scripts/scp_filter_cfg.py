#!/usr/bin/env python3
"""Filter a Broad Single Cell Portal bulk-download curl config (cfg.txt).

SCP's "Bulk download" button hands you a cfg.txt whose url=/output= stanzas
carry signed Google Storage links that expire after about one day. This
script drops stanzas whose output path matches --exclude (default: the
*.pickle Puck objects, which are redundant with the h5ad files and hold
most of the bytes), and optionally keeps only those matching --include.

Usage:
    python3 scp_filter_cfg.py cfg.txt cfg_filtered.txt
    python3 scp_filter_cfg.py cfg.txt cfg_filtered.txt --exclude '\\.pickle$|digital_expression'
Then:
    curl -K cfg_filtered.txt
"""
import argparse
import re


def stanzas(text):
    """Split cfg into header lines and (url, output, raw) blocks."""
    header, blocks = [], []
    cur = []
    for line in text.splitlines():
        if line.startswith("url="):
            if cur:
                blocks.append(cur)
            cur = [line]
        elif line.startswith("output=") and cur:
            cur.append(line)
            blocks.append(cur)
            cur = []
        elif cur:
            cur.append(line)
        elif line.strip():
            header.append(line)
    if cur:
        blocks.append(cur)
    return header, blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cfg_in")
    ap.add_argument("cfg_out")
    ap.add_argument("--exclude", default=r"\.pickle$")
    ap.add_argument("--include", default=None)
    args = ap.parse_args()

    with open(args.cfg_in, encoding="utf-8") as fh:
        header, blocks = stanzas(fh.read())
    exc = re.compile(args.exclude) if args.exclude else None
    inc = re.compile(args.include) if args.include else None

    kept, dropped = [], []
    for b in blocks:
        out_line = next((l for l in b if l.startswith("output=")), "")
        path = out_line[len("output="):].strip().strip('"')
        if (exc and exc.search(path)) or (inc and not inc.search(path)):
            dropped.append(path)
        else:
            kept.append(b)

    with open(args.cfg_out, "w", encoding="utf-8") as fh:
        for h in header:
            fh.write(h + "\n\n")
        for b in kept:
            fh.write("\n".join(b) + "\n\n")

    print(f"stanzas in: {len(blocks)}  kept: {len(kept)}  dropped: {len(dropped)}")
    for p in dropped:
        print(f"  dropped {p}")
    exp = sorted(set(re.findall(r"Expires=(\d+)", "\n".join("\n".join(b) for b in kept))))
    if exp:
        import datetime
        t = datetime.datetime.fromtimestamp(int(exp[0]), datetime.timezone.utc)
        print(f"signed URLs expire at {t:%Y-%m-%d %H:%M} UTC -- run the download before then")


if __name__ == "__main__":
    main()
