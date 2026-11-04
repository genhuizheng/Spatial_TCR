#!/usr/bin/env python3
"""Convert MiXCR 4 10x-sc-xcr-vdj output to the clonotype table read by link_spot_sctcr.py.

Input: result.clones.tsv from `mixcr analyze 10x-sc-xcr-vdj` (one row per clone and cell
barcode: cloneId, cellGroup, tagValueCELL, topChains, nSeqCDR3, aaSeqCDR3, all*HitsWithScore).
A clonotype is a MiXCR cell group (clones assembled into the same cells, so TRA and TRB are
paired); clones outside any group become single-chain clonotypes "clone<cloneId>".
n_cells = distinct cell barcodes over all clones of the clonotype. If --groups is given
(result.clone.groups_TRAB.tsv), these counts are checked against groupUniqueCellCount.

Output columns: sample clonotype_id n_cells chain cdr3_nt cdr3_aa v_gene j_gene productive
umis cells_with_chain
"""
import argparse
import re
import sys
from collections import defaultdict


def top(hits):
    return re.sub(r"[*(].*", "", (hits or "").split(",")[0]).strip()


def grouped(g):
    return bool(re.fullmatch(r"\d+", (g or "").strip()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", required=True)
    ap.add_argument("--clones", required=True, help="MiXCR result.clones.tsv")
    ap.add_argument("--groups", default=None, help="MiXCR result.clone.groups_TRAB.tsv (cell count check)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    need = ["cloneId", "cellGroup", "tagValueCELL", "nSeqCDR3", "aaSeqCDR3", "allVHitsWithScore",
            "allJHitsWithScore", "uniqueMoleculeCount"]
    cells = defaultdict(set)                       # clonotype -> cell barcodes
    chains = {}                                    # (clonotype, chain, nt) -> record
    n_rows = n_other = 0
    with open(args.clones) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        missing = [c for c in need if c not in cols]
        if missing:
            sys.exit(f"{args.clones}: missing columns {missing}")
        for line in fh:
            f = dict(zip(cols, line.rstrip("\n").split("\t")))
            n_rows += 1
            v = top(f["allVHitsWithScore"])
            chain = f.get("topChains") or v[:3]
            if chain not in ("TRA", "TRB") or not f["nSeqCDR3"]:
                n_other += 1
                continue
            ct = f["cellGroup"].strip() if grouped(f["cellGroup"]) else "clone" + f["cloneId"]
            cells[ct].add(f["tagValueCELL"])
            key = (ct, chain, f["nSeqCDR3"])
            r = chains.setdefault(key, {"aa": f["aaSeqCDR3"], "v": v, "j": top(f["allJHitsWithScore"]),
                                        "umis": 0, "cells": set()})
            r["umis"] += int(float(f["uniqueMoleculeCount"] or 0))
            r["cells"].add(f["tagValueCELL"])

    with open(args.out, "w") as fh:
        fh.write("sample\tclonotype_id\tn_cells\tchain\tcdr3_nt\tcdr3_aa\tv_gene\tj_gene\tproductive\tumis\t"
                 "cells_with_chain\n")
        for (ct, chain, nt), r in sorted(chains.items(), key=lambda kv: (-len(cells[kv[0][0]]), kv[0])):
            productive = "no" if ("_" in r["aa"] or "*" in r["aa"]) else "yes"
            fh.write("\t".join(map(str, [args.sample, ct, len(cells[ct]), chain, nt, r["aa"], r["v"], r["j"],
                                         productive, r["umis"], len(r["cells"])])) + "\n")

    groups = {c for c in cells if not c.startswith("clone")}
    paired = {c for c in groups if {k[1] for k in chains if k[0] == c} >= {"TRA", "TRB"}}
    print(f"{args.sample}: {n_rows} clone-cell rows ({n_other} not TRA/TRB); {len(cells)} clonotypes "
          f"({len(groups)} cell groups, {len(paired)} with TRA+TRB; {len(cells) - len(groups)} ungrouped clones); "
          f"{len(set().union(*cells.values())) if cells else 0} cells")

    if args.groups:
        ref = {}
        with open(args.groups) as fh:
            cols = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                f = dict(zip(cols, line.rstrip("\n").split("\t")))
                if grouped(f.get("cellGroup")):
                    ref[f["cellGroup"].strip()] = int(float(f.get("groupUniqueCellCount") or 0))
        same = sum(1 for g in groups if g in ref and ref[g] == len(cells[g]))
        print(f"  cell count check vs {args.groups.split('/')[-1]}: {same} of {len(groups)} groups agree, "
              f"{len(groups - set(ref))} groups missing there, {len(set(ref) - groups)} only there")


if __name__ == "__main__":
    main()
