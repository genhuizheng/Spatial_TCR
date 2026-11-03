#!/usr/bin/env python3
"""Spot x clone TCR UMI counts for Visium TCR-enriched libraries (Hudson and Sudmeier 2022).

Python 3 port of code_samples/combine_counts.py from github.com/whhudson/spatialTCR
(the published method for GSE179572 / PRJNA742564). Counting rules are unchanged:
  1. A read 2 belongs to a clone if MiXCR exportReadsForClones wrote it to
     reads_cln<N>.fastq.gz. Reads written for more than one clone are dropped.
  2. Read 1 carries the spot barcode (bases 1-16) and UMI (bases 17-28).
  3. Read 1 records are taken in file order; the first read of each (barcode, UMI)
     pair is counted and later reads with the same pair are ignored, whatever clone
     they support (the authors' "rudimentary" UMI collapse, no error correction).
  4. Only barcodes listed in the Space Ranger positions file are counted.
Changes, none of which alter counts on the authors' own data:
  - Mates are paired by the first word of the read name. The original replaced
    "1:N:0" with "2:N:0", which never matches ENA/SRA names such as
    "SRR15052440.1 1/1" and "SRR15052440.1 1/2" (it would count nothing).
  - FASTQ is parsed four lines per record. The original treated any line starting
    with "@" as a header, so quality strings starting with "@" became fake reads.
  - Both positions formats are read: tissue_positions_list.csv (no header) and
    tissue_positions.csv (Space Ranger 2.0+, with header).
Outputs:
  --matrix  spot x clone table in the authors' layout (header row of clone names,
            one row per spot), for direct comparison with their output_counts.txt
  --long    one row per spot and clone with UMI count > 0, plus spot position and
            clone annotation from the MiXCR clones table (if --clones is given)
"""
import argparse
import glob
import gzip
import os
import re
import sys
from collections import defaultdict


def fastq_names(path):
    """Yield (read_id, sequence) with read_id = first word of the header, no '@'."""
    with gzip.open(path, "rt") as fh:
        while True:
            head = fh.readline()
            if not head:
                return
            seq = fh.readline()
            fh.readline()
            fh.readline()
            if not head.startswith("@"):
                sys.exit(f"malformed FASTQ record in {path}: {head[:60]!r}")
            yield head[1:].split()[0], seq.rstrip("\n")


def read_positions(path):
    """barcode (without -1) -> (in_tissue, array_row, array_col, pxl_row, pxl_col)."""
    pos = {}
    with open(path) as fh:
        for line in fh:
            f = line.rstrip("\n").split(",")
            if f[0] == "barcode":
                continue
            pos[re.sub(r"-1$", "", f[0])] = tuple(f[1:6])
    return pos


def read_clones(path):
    """cloneId -> dict of selected MiXCR export columns."""
    if not path:
        return {}
    keep = ["cloneCount", "aaSeqCDR3", "nSeqCDR3", "allVHitsWithScore", "allDHitsWithScore",
            "allJHitsWithScore", "allCHitsWithScore"]
    out = {}
    with open(path) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(cols)}
        for line in fh:
            f = line.rstrip("\n").split("\t")
            rec = {c: (f[idx[c]] if c in idx and idx[c] < len(f) else "") for c in keep}
            top_v = rec["allVHitsWithScore"].split(",")[0]
            rec["chain"] = top_v[:3] if top_v else ""
            for c in ("allVHitsWithScore", "allDHitsWithScore", "allJHitsWithScore", "allCHitsWithScore"):
                rec[c] = re.sub(r"\*.*", "", rec[c].split(",")[0])  # top hit, gene name only
            out[f[idx["cloneId"]]] = rec
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reads-dir", required=True, help="folder of MiXCR reads_cln<N>.fastq.gz")
    ap.add_argument("--r1", required=True, nargs="+", help="read 1 FASTQ(.gz) file(s)")
    ap.add_argument("--positions", required=True, help="Space Ranger tissue_positions(_list).csv")
    ap.add_argument("--clones", default=None, help="MiXCR clones table (exportClones) for annotation")
    ap.add_argument("--matrix", default=None, help="output: spot x clone matrix (authors' layout)")
    ap.add_argument("--long", default=None, help="output: long table of nonzero spot-clone UMI counts")
    args = ap.parse_args()

    positions = read_positions(args.positions)

    clone_files = sorted(glob.glob(os.path.join(args.reads_dir, "*_cln*.fastq.gz")),
                         key=lambda p: int(re.search(r"_cln(\d+)\.", p).group(1)))
    if not clone_files:
        sys.exit(f"no reads_cln<N>.fastq.gz in {args.reads_dir}")
    read_to_clone = {}
    dup = set()
    n_clone_reads = 0
    clones = []
    for path in clone_files:
        clone = re.search(r"_cln(\d+)\.", path).group(1)
        clones.append(clone)
        for rid, _ in fastq_names(path):
            n_clone_reads += 1
            if rid in read_to_clone or rid in dup:
                dup.add(rid)
                read_to_clone.pop(rid, None)
            else:
                read_to_clone[rid] = clone

    counts = defaultdict(lambda: defaultdict(int))
    seen_umi = set()
    stats = defaultdict(int)
    for path in args.r1:
        for rid, seq in fastq_names(path):
            stats["r1_reads"] += 1
            clone = read_to_clone.get(rid)
            if clone is None:
                continue
            stats["r1_with_clone"] += 1
            bc, umi = seq[0:16], seq[16:28]
            if (bc, umi) in seen_umi:
                stats["duplicate_umi"] += 1
                continue
            seen_umi.add((bc, umi))
            if bc in positions:
                counts[bc][clone] += 1
                stats["umis_on_spots"] += 1
            else:
                stats["umis_off_list"] += 1

    if args.matrix:
        with open(args.matrix, "w") as fh:
            fh.write("\t".join("clone" + c for c in clones) + "\n")
            for bc in positions:
                fh.write(bc + "\t" + "\t".join(str(counts[bc][c]) if bc in counts else "0" for c in clones) + "\n")
    if args.long:
        ann = read_clones(args.clones)
        ann_cols = ["chain", "aaSeqCDR3", "nSeqCDR3", "allVHitsWithScore", "allDHitsWithScore",
                    "allJHitsWithScore", "allCHitsWithScore", "cloneCount"]
        with open(args.long, "w") as fh:
            fh.write("\t".join(["barcode", "in_tissue", "array_row", "array_col", "pxl_row", "pxl_col",
                                "clone_id", "umi_count", "chain", "cdr3_aa", "cdr3_nt", "v_gene", "d_gene",
                                "j_gene", "c_gene", "mixcr_clone_count"]) + "\n")
            for bc in positions:
                if bc not in counts:
                    continue
                for c in clones:
                    n = counts[bc].get(c, 0)
                    if n:
                        a = ann.get(c, {})
                        fh.write("\t".join([bc + "-1", *positions[bc], c, str(n)] +
                                           [a.get(k, "") for k in ann_cols]) + "\n")

    print(f"clones: {len(clones)}; clone reads: {n_clone_reads}; reads in >1 clone dropped: {len(dup)}")
    print("r1 reads: {r1_reads}; with a clone: {r1_with_clone}; duplicate barcode+UMI: {duplicate_umi}; "
          "UMIs on listed spots: {umis_on_spots}; UMIs with unlisted barcode: {umis_off_list}".format(
              **{k: stats[k] for k in ("r1_reads", "r1_with_clone", "duplicate_umi", "umis_on_spots", "umis_off_list")}))
    print(f"spots with >=1 TCR UMI: {len(counts)} of {len(positions)}")


if __name__ == "__main__":
    main()
