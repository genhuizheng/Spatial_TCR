#!/usr/bin/env python3
"""TCR probe calls for one Xenium section following McCord et al. 2026, with their mismatched-probe
negative control made quantitative.

McCord et al. (PMC13138865) clustered Xenium gene expression without supervision (Seurat), labelled
the clusters from lineage transcripts, and called a TCR probe successful if it was "detected in at
least five T cells" and "enriched within the T cell Xenium gene expression cluster"; probes of
other patients on the same slide served as internal negative controls. No per-cell count
threshold was published. This script reproduces that rule:

  1. Clusters: genes only (TCR probes and controls excluded, so the T label is TCR-independent);
     normalize_total 1e4, log1p, scale (max 10), PCA 30, kNN graph (k = 20, 30 PCs), Leiden
     (scanpy; Seurat's default is Louvain, so this is a documented deviation). Cells without gene
     counts are not clustered. Each cluster is labelled with the lineage whose marker score (mean
     z-scored log expression of that lineage's markers present in the panel, >= 2 needed) is
     highest on average; --labels overrides this with a hand-checked cluster -> label table.
  2. Probe rule (McCord): detected (count >= 1) in >= --min-t-cells T-cluster cells and enriched in
     T-cluster cells over other clustered cells (one-sided Fisher exact test, Benjamini-Hochberg
     FDR < --alpha, computed separately for own and other-patient probes).
  3. Negative control: the same rule applied to the other patients' probes estimates how often it
     passes probes that cannot be real in this patient. As a sensitivity tier ("strict"), an own
     probe must also have a larger T-cell excess (detection rate in T-cluster cells minus the rate
     in other clustered cells, so probes that stick everywhere score about 0) than every
     same-chain other-patient probe on the slide (equivalently empirical p = 1 / (1 + #controls),
     the smallest possible; reported as null_p = (1 + #controls with excess >= probe) /
     (1 + #controls)). Controls get the same leave-one-out comparison as a calibration check.

Focal TCR cells: T-cluster cells with >= 1 count of a passing own probe (tier_mccord), and of a
strict own probe (tier_strict). Outputs: clusters.tsv, cluster_summary.tsv, probe_calls.tsv,
cell_calls.tsv, calls_config.json. xenium_shells.py --calls <out> uses them.
"""
import argparse
import json
import os
import sys
import time

import numpy as np
from scipy.stats import fisher_exact

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xenium_shells import feature_classes, read_10x_h5, read_parquet, write_tsv  # noqa: E402

LINEAGES = {
    "T": ["CD3D", "CD3E", "CD3G", "CD2", "CD247", "CD8A", "CD4", "TRAC"],
    "B": ["MS4A1", "CD79A", "CD79B", "CD19", "BANK1"],
    "plasma": ["JCHAIN", "MZB1", "IGHG1", "CD38"],
    "myeloid": ["CD68", "CD163", "CD14", "LYZ", "CSF1R", "ITGAX", "C1QA"],
    "granulocyte": ["CSF3R", "FCGR3B", "CXCR2", "S100A8"],
    "mast": ["TPSAB1", "KIT", "CPA3"],
    "endothelial": ["PECAM1", "VWF", "CDH5", "CLDN5"],
    "fibroblast": ["COL1A1", "COL1A2", "DCN", "LUM", "PDGFRA", "PDGFRB"],
    "epithelial": ["EPCAM", "KRT5", "KRT14", "KRT17", "KRT8", "KRT18", "SFN"],
}


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    if not n:
        return p
    order = np.argsort(p)
    q = p[order] * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(q, 1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--probe-group", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-t-cells", type=int, default=5, help="McCord: detected in at least five T cells")
    ap.add_argument("--alpha", type=float, default=0.05, help="BH FDR for T-cluster enrichment")
    ap.add_argument("--resolution", type=float, default=0.8, help="Leiden resolution (Seurat FindClusters default 0.8)")
    ap.add_argument("--labels", default=None, help="TSV cluster<TAB>label overriding the automatic labels")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    import scanpy as sc
    import anndata as ad
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)

    X, barcodes, feats = read_10x_h5(args.prefix + "_cell_feature_matrix.h5")
    cells = read_parquet(args.prefix + "_cells.parquet.gz").to_pydict()
    keep = set(cells["cell_id"])
    idx = [i for i, b in enumerate(barcodes) if b in keep]
    X = X[idx]; barcodes = [barcodes[i] for i in idx]
    cls, chain, cdr3, pgroup = feature_classes(feats, args.probe_group)
    names = np.array(feats["name"])
    gene_cols = np.where(cls == "gene")[0]
    G = X[:, gene_cols].astype(np.float32)
    gtot = np.asarray(G.sum(axis=1)).ravel()
    clustered = gtot > 0
    print(f"{args.sample}: {X.shape[0]} cells, {len(gene_cols)} genes; clustering {int(clustered.sum())} cells with gene counts")

    a = ad.AnnData(G[clustered].tocsr())
    a.var_names = names[gene_cols]
    a.obs_names = [barcodes[i] for i in np.where(clustered)[0]]
    sc.pp.normalize_total(a, target_sum=1e4)
    sc.pp.log1p(a)
    a.layers["lognorm"] = a.X.copy()
    sc.pp.scale(a, max_value=10)
    Z = np.asarray(a.X)
    n_pcs = min(30, a.n_vars - 1)
    sc.tl.pca(a, n_comps=n_pcs, random_state=args.seed)
    sc.pp.neighbors(a, n_neighbors=20, n_pcs=n_pcs, random_state=args.seed)
    sc.tl.leiden(a, resolution=args.resolution, flavor="igraph", n_iterations=2, random_state=args.seed)
    a.X = a.layers["lognorm"]
    used = {}
    vn = list(a.var_names)
    for lin, genes in LINEAGES.items():
        g = [x for x in genes if x in vn]
        if len(g) >= 2:
            used[lin] = g
    lins = list(used)
    if not lins:
        sys.exit("no lineage has >= 2 marker genes in the panel")
    S = np.c_[[Z[:, [vn.index(x) for x in used[l]]].mean(axis=1) for l in lins]].T
    clus = a.obs["leiden"].astype(str).values
    cl_ids = sorted(set(clus), key=int)
    auto = {c: lins[int(np.argmax(S[clus == c].mean(axis=0)))] for c in cl_ids}
    labels = dict(auto)
    if args.labels:
        with open(args.labels) as fh:
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) >= 2 and f[0] in labels:
                    labels[f[0]] = f[1]
    summ = []
    tm = [x for x in used.get("T", [])]
    tmark = np.asarray((a.layers["lognorm"][:, [list(a.var_names).index(x) for x in tm]] > 0).sum(axis=1)).ravel() > 0 if tm else np.zeros(a.n_obs, bool)
    print("   cluster  n_cells  label        auto_label   frac_T_marker  " + "  ".join(f"{l[:6]:>6}" for l in lins))
    for c in cl_ids:
        m = clus == c
        sc_mean = S[m].mean(axis=0)
        summ.append([c, int(m.sum()), labels[c], auto[c], float(tmark[m].mean())] + [float(v) for v in sc_mean])
        print(f"   {c:>7}  {int(m.sum()):7d}  {labels[c]:<11}  {auto[c]:<11}  {tmark[m].mean():13.2f}  " +
              "  ".join(f"{v:6.2f}" for v in sc_mean))
    write_tsv(os.path.join(args.out, "cluster_summary.tsv"),
              ["cluster", "n_cells", "label", "auto_label", "frac_T_marker"] + [f"mean_score_{l}" for l in lins], summ)

    cluster_of = np.full(X.shape[0], "", dtype=object)
    cluster_of[np.where(clustered)[0]] = clus
    label_of = np.array([labels.get(c, "unclustered") if c else "unclustered" for c in cluster_of], dtype=object)
    isT = label_of == "T"
    write_tsv(os.path.join(args.out, "clusters.tsv"), ["cell_id", "cluster", "label", "gene_counts"],
              [[barcodes[i], cluster_of[i], label_of[i], int(gtot[i])] for i in range(X.shape[0])])
    nT, nN = int((isT & clustered).sum()), int((~isT & clustered).sum())
    print(f"T-cluster cells: {nT} of {int(clustered.sum())} clustered ({nT / max(1, clustered.sum()):.1%})")
    if not nT:
        sys.exit("no T cluster; check cluster_summary.tsv and pass --labels")

    # probe tests
    tcr = np.where((cls == "tcr_own") | (cls == "tcr_other"))[0]
    Xc = X.tocsc()
    rec = {}
    for k in tcr:
        det = np.zeros(X.shape[0], bool)
        det[Xc[:, k].nonzero()[0]] = True
        dT = int((det & isT).sum()); dN = int((det & ~isT & clustered).sum())
        p = fisher_exact([[dT, nT - dT], [dN, nN - dN]], alternative="greater")[1]
        rec[k] = dict(det=det, dT=dT, dN=dN, d_uncl=int((det & ~clustered).sum()), rate=dT / nT,
                      excess=dT / nT - (dN / nN if nN else 0.0),
                      fold=(dT / nT) / (dN / nN) if dN else float("inf"), p=p)
    for group in ("tcr_own", "tcr_other"):
        ks = [k for k in tcr if cls[k] == group]
        for k, q in zip(ks, bh([rec[k]["p"] for k in ks])):
            rec[k]["fdr"] = q
            rec[k]["mccord"] = rec[k]["dT"] >= args.min_t_cells and q < args.alpha
    for k in tcr:
        ctrl = [j for j in tcr if cls[j] == "tcr_other" and chain[j] == chain[k] and j != k]
        rec[k]["n_ctrl"] = len(ctrl)
        rec[k]["null_p"] = (1 + sum(rec[j]["excess"] >= rec[k]["excess"] for j in ctrl)) / (1 + len(ctrl)) if ctrl else float("nan")
        rec[k]["max_ctrl"] = max((rec[j]["excess"] for j in ctrl), default=float("nan"))
        rec[k]["strict"] = rec[k]["mccord"] and bool(ctrl) and rec[k]["excess"] > rec[k]["max_ctrl"]
    rows = []
    for k in sorted(tcr, key=lambda k: (cls[k] != "tcr_own", chain[k], -rec[k]["dT"])):
        r = rec[k]
        rows.append([names[k], cls[k], chain[k], cdr3[k], pgroup[k], int(r["det"].sum()), r["dT"], r["dN"], r["d_uncl"],
                     r["rate"], r["excess"], r["fold"], r["p"], r["fdr"], "yes" if r["mccord"] else "no", r["n_ctrl"],
                     r["max_ctrl"], r["null_p"], "yes" if r["strict"] else "no"])
    write_tsv(os.path.join(args.out, "probe_calls.tsv"),
              ["probe", "class", "chain", "cdr3_aa", "probe_group", "n_cells", "n_T_cells", "n_nonT_cells",
               "n_unclustered_cells", "T_detection_rate", "T_excess", "T_enrichment_fold", "fisher_p", "fdr",
               "mccord_pass", "n_same_chain_controls", "max_control_T_excess", "null_p", "strict_pass"], rows)
    for group in ("tcr_own", "tcr_other"):
        for ch in sorted({chain[k] for k in tcr if cls[k] == group}):
            ks = [k for k in tcr if cls[k] == group and chain[k] == ch]
            print(f"   {group:9} {ch}: {len(ks):3d} probes, McCord rule passed {sum(rec[k]['mccord'] for k in ks):3d}, "
                  f"strict {sum(rec[k]['strict'] for k in ks):3d}"
                  + (" (controls: leave-one-out, so the top control can pass)" if group == "tcr_other" else ""))

    own_m = [k for k in tcr if cls[k] == "tcr_own" and rec[k]["mccord"]]
    own_s = [k for k in own_m if rec[k]["strict"]]
    other = [k for k in tcr if cls[k] == "tcr_other"]
    cr = []
    nm = ns = 0
    for i in range(X.shape[0]):
        pm = [f"{names[k]}:{Xc[i, k]}" for k in own_m if rec[k]["det"][i]]
        if not pm and not any(rec[k]["det"][i] for k in other):
            continue
        ps = [s for s, k in zip(pm, [k for k in own_m if rec[k]["det"][i]]) if rec[k]["strict"]]
        po = [f"{names[k]}:{Xc[i, k]}" for k in other if rec[k]["det"][i]]
        tm_ = "yes" if (isT[i] and pm) else "no"
        ts_ = "yes" if (isT[i] and ps) else "no"
        nm += tm_ == "yes"; ns += ts_ == "yes"
        cr.append([barcodes[i], cluster_of[i], label_of[i], ";".join(pm), ";".join(ps), ";".join(po), tm_, ts_])
    write_tsv(os.path.join(args.out, "cell_calls.tsv"),
              ["cell_id", "cluster", "label", "own_mccord_probes", "own_strict_probes", "other_patient_probes",
               "tier_mccord", "tier_strict"], cr)
    nonT = sum(1 for r in cr if r[3] and r[6] == "no")
    print(f"focal TCR cells: tier_mccord {nm}, tier_strict {ns}; cells with a passing own probe outside the T cluster: {nonT}")
    with open(os.path.join(args.out, "calls_config.json"), "w") as fh:
        json.dump(dict(sample=args.sample, prefix=args.prefix, probe_group=args.probe_group, min_t_cells=args.min_t_cells,
                       alpha=args.alpha, strict_rule="T excess > every same-chain control", resolution=args.resolution, n_pcs=n_pcs,
                       n_neighbors=20, labels_file=args.labels, lineage_markers_used=used, seed=args.seed,
                       scanpy=sc.__version__, anndata=ad.__version__,
                       created=time.strftime("%Y-%m-%dT%H:%M:%S")), fh, indent=1)
    print(f"{args.sample}: calls done in {time.time() - t0:.0f} s -> {args.out}")


if __name__ == "__main__":
    main()
