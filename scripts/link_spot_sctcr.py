#!/usr/bin/env python3
"""Link Visium spot TRB clones (visium_tcr_counts.py --long) to matched single-cell clonotypes.

A spot clone links to a single-cell clonotype when their TRB CDR3 nucleotide sequences are
identical ("nt"); identical CDR3 amino acids with a different nucleotide sequence are reported
separately ("aa") and are not used for spot annotation. Every Visium patient is compared with
every single-cell sample: pairs where the sample contains that patient are "expected", all
others are "cross" pairs, whose match rate is the negative control for chance or public
CDR3 sharing (the same logic as McCord's mismatched-patient probes).
Pooled single-cell captures hold several patients. A pooled clonotype is attributed to a
patient only if its TRB nt CDR3 is seen in exactly one of the pool's patients' Visium data;
clonotypes seen in more than one are reported as shared and not attributed.

Single-cell input (--sc, one or more TSV), one row per clonotype and chain:
    sample  clonotype_id  n_cells  chain  cdr3_nt  cdr3_aa  v_gene  j_gene
(written from the MiXCR 10x output by the adapter step; chain is TRA or TRB).

Outputs in --out: clone_links.tsv, spot_links.tsv, link_summary.tsv
"""
import argparse
import os
import re
import sys
from collections import defaultdict


def gene(v):
    return re.sub(r"\*.*", "", v or "").strip()


def read_sheet(path):
    """sc sample -> set of patient numbers (as strings)."""
    out = {}
    with open(path) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = dict(zip(cols, line.rstrip("\n").split("\t")))
            out[f["sample"]] = {p.strip() for p in f["patients"].split(",")}
    return out


def read_spots(path, in_tissue_only):
    """Spot TRB rows and per-clone (cdr3_nt) totals."""
    rows, clones = [], {}
    with open(path) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = dict(zip(cols, line.rstrip("\n").split("\t")))
            if f["chain"] != "TRB" or not f["cdr3_nt"]:
                continue
            if in_tissue_only and f["in_tissue"] != "1":
                continue
            rows.append(f)
            c = clones.setdefault(f["cdr3_nt"], {"cdr3_aa": f["cdr3_aa"], "v": set(), "umis": 0, "spots": set()})
            c["v"].add(gene(f["v_gene"]))
            c["umis"] += int(f["umi_count"])
            c["spots"].add(f["barcode"])
    return rows, clones


def read_sc(paths):
    """sample -> clonotype_id -> {n_cells, TRB: [...], TRA: [...]}."""
    sc = defaultdict(dict)
    need = ["sample", "clonotype_id", "n_cells", "chain", "cdr3_nt", "cdr3_aa", "v_gene", "j_gene"]
    for path in paths:
        with open(path) as fh:
            cols = fh.readline().rstrip("\n").split("\t")
            missing = [c for c in need if c not in cols]
            if missing:
                sys.exit(f"{path}: missing columns {missing}")
            for line in fh:
                f = dict(zip(cols, line.rstrip("\n").split("\t")))
                if f["chain"] not in ("TRA", "TRB") or not f["cdr3_nt"]:
                    continue
                ct = sc[f["sample"]].setdefault(f["clonotype_id"], {"n_cells": int(f["n_cells"]), "TRA": [], "TRB": []})
                ct["TRA" if f["chain"] == "TRA" else "TRB"].append(
                    {"nt": f["cdr3_nt"], "aa": f["cdr3_aa"], "v": gene(f["v_gene"]), "j": gene(f["j_gene"])})
    return sc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spots", required=True, nargs="+", metavar="PATIENT=PATH",
                    help="Visium spot_clone_long.tsv per patient, e.g. 16=outputs/visium_tcr/pt16/spot_clone_long.tsv")
    ap.add_argument("--sc", required=True, nargs="+", help="single-cell clonotype TSV(s)")
    ap.add_argument("--sheet", default="metadata/bm_sctcr_samples.tsv")
    ap.add_argument("--out", required=True)
    ap.add_argument("--include-outside-tissue", action="store_true")
    args = ap.parse_args()

    sheet = read_sheet(args.sheet)
    sc = read_sc(args.sc)
    for s in sc:
        if s not in sheet:
            sys.exit(f"single-cell sample {s} not in {args.sheet}")
    visium = {}
    for item in args.spots:
        p, path = item.split("=", 1)
        visium[p] = read_spots(path, not args.include_outside_tissue)

    # TRB indexes per single-cell sample
    by_nt, by_aa = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: defaultdict(list))
    for s, cts in sc.items():
        for cid, ct in cts.items():
            for b in ct["TRB"]:
                by_nt[s][b["nt"]].append(cid)
                by_aa[s][b["aa"]].append(cid)

    # for pools: in how many of the pool's Visium patients is each nt CDR3 present
    def n_pool_patients(s, nt):
        return sum(1 for p in sheet[s] if p in visium and nt in visium[p][1])

    os.makedirs(args.out, exist_ok=True)
    links = []
    for p, (_, clones) in visium.items():
        for nt, c in clones.items():
            for s in sc:
                pair = "expected" if p in sheet[s] else "cross"
                hits = [(cid, "nt") for cid in dict.fromkeys(by_nt[s].get(nt, []))]
                hits += [(cid, "aa") for cid in dict.fromkeys(by_aa[s].get(c["cdr3_aa"], []))
                         if (cid, "nt") not in hits]
                for cid, kind in hits:
                    ct = sc[s][cid]
                    sc_v = sorted({b["v"] for b in ct["TRB"]})
                    npp = n_pool_patients(s, nt) if pair == "expected" else 0
                    links.append({
                        "visium_patient": p, "cdr3_nt": nt, "cdr3_aa": c["cdr3_aa"],
                        "visium_v": ",".join(sorted(c["v"])), "spot_umis": c["umis"], "n_spots": len(c["spots"]),
                        "sc_sample": s, "sc_patients": ",".join(sorted(sheet[s], key=int)), "pair": pair,
                        "match": kind, "sc_clonotype": cid, "sc_cells": ct["n_cells"], "sc_trb_v": ",".join(sc_v),
                        "v_agree": "yes" if c["v"] & set(sc_v) else "no",
                        "tra_cdr3_aa": ",".join(a["aa"] for a in ct["TRA"]),
                        "tra_cdr3_nt": ",".join(a["nt"] for a in ct["TRA"]),
                        "tra_v": ",".join(a["v"] for a in ct["TRA"]),
                        "pool_patients_with_cdr3": npp,
                        "attributed": "yes" if pair == "expected" and kind == "nt" and npp == 1 else "no"})

    cols = ["visium_patient", "cdr3_nt", "cdr3_aa", "visium_v", "spot_umis", "n_spots", "sc_sample", "sc_patients",
            "pair", "match", "sc_clonotype", "sc_cells", "sc_trb_v", "v_agree", "tra_cdr3_aa", "tra_cdr3_nt",
            "tra_v", "pool_patients_with_cdr3", "attributed"]
    with open(os.path.join(args.out, "clone_links.tsv"), "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in links:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    # spot annotation: attributed nt links only
    ann = defaultdict(list)
    for r in links:
        if r["attributed"] == "yes":
            ann[(r["visium_patient"], r["cdr3_nt"])].append(r)
    with open(os.path.join(args.out, "spot_links.tsv"), "w") as fh:
        fh.write("\t".join(["visium_patient", "barcode", "in_tissue", "array_row", "array_col", "pxl_row", "pxl_col",
                            "cdr3_nt", "cdr3_aa", "v_gene", "umi_count", "sc_links", "tra_cdr3_aa", "tra_v"]) + "\n")
        for p, (rows, _) in visium.items():
            for f in rows:
                a = ann.get((p, f["cdr3_nt"]), [])
                fh.write("\t".join([p, f["barcode"], f["in_tissue"], f["array_row"], f["array_col"], f["pxl_row"],
                                    f["pxl_col"], f["cdr3_nt"], f["cdr3_aa"], gene(f["v_gene"]), f["umi_count"],
                                    ";".join(f"{r['sc_sample']}:{r['sc_clonotype']}" for r in a),
                                    ";".join(r["tra_cdr3_aa"] for r in a),
                                    ";".join(r["tra_v"] for r in a)]) + "\n")

    # summary per Visium patient x single-cell sample
    with open(os.path.join(args.out, "link_summary.tsv"), "w") as fh:
        fh.write("visium_patient\tsc_sample\tpair\tvisium_trb_clones\tvisium_trb_umis\tclones_nt\tclones_aa_only\t"
                 "umis_nt\tfrac_umis_nt\tclones_attributed\tumis_attributed\tclones_shared_in_pool\t"
                 "sc_clonotypes_nt\tsc_cells_nt\tsc_clonotypes_total\n")
        for p, (_, clones) in visium.items():
            tot_umis = sum(c["umis"] for c in clones.values())
            for s in sc:
                rs = [r for r in links if r["visium_patient"] == p and r["sc_sample"] == s]
                nt_cl = {r["cdr3_nt"] for r in rs if r["match"] == "nt"}
                aa_cl = {r["cdr3_nt"] for r in rs if r["match"] == "aa"} - nt_cl
                att = {r["cdr3_nt"] for r in rs if r["attributed"] == "yes"}
                shared = {r["cdr3_nt"] for r in rs if r["match"] == "nt" and r["pool_patients_with_cdr3"] > 1}
                umis_nt = sum(clones[n]["umis"] for n in nt_cl)
                sc_ids = {r["sc_clonotype"] for r in rs if r["match"] == "nt"}
                fh.write("\t".join(map(str, [
                    p, s, "expected" if p in sheet[s] else "cross", len(clones), tot_umis, len(nt_cl), len(aa_cl),
                    umis_nt, f"{umis_nt / tot_umis:.3f}" if tot_umis else "NA", len(att),
                    sum(clones[n]["umis"] for n in att), len(shared), len(sc_ids),
                    sum(sc[s][i]["n_cells"] for i in sc_ids), len(sc[s])])) + "\n")
    print(open(os.path.join(args.out, "link_summary.tsv")).read(), end="")


if __name__ == "__main__":
    main()
