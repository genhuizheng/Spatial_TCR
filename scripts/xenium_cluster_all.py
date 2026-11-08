#!/usr/bin/env python3
"""Joint clustering of all GSE300147 Xenium sections, following McCord et al. 2026.

McCord et al. clustered the Xenium gene expression of all sections without supervision ("UMAP and
nearest-neighbor clustering", Seurat) into ten clusters and labelled them by lineage transcripts
(T, B, myeloid, endothelial, fibroblast, granulocyte, two malignant and two normal epithelial).
This script does the same once for every section in --sheet, so that the T cluster used by the
probe rule (xenium_tcr_calls.py --clusters) is shared across sections:

  genes only (TCR probes, controls and features not present in every section excluded); cells with
  gene counts; normalize_total 1e4, log1p, scale (max 10), PCA 30, kNN k = 20, Leiden (scanpy,
  igraph flavour) at each --resolutions value. The resolution whose cluster count is closest to
  --target (10, as published; ties go to the lower resolution) is kept. No batch correction, as
  none is described.

Outputs: resolution_scan.tsv, clusters.tsv (sample, cell_id, cluster), cluster_summary.tsv (cells
per cluster and section, lineage marker scores, top genes, proposed label), labels_proposed.tsv
(cluster -> proposed label; copy to labels.tsv and correct by hand before the probe calls).
"""
import argparse
import json
import os
import sys
import time

import numpy as np
from scipy import sparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xenium_shells import feature_classes, read_10x_h5, read_parquet, write_tsv  # noqa: E402
from xenium_tcr_calls import LINEAGES  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--out", required=True)
    ap.add_argument("--resolutions", default="0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.8,1.0")
    ap.add_argument("--target", type=int, default=10, help="published number of clusters")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    import anndata as ad
    import scanpy as sc
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)

    with open(args.sheet) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        sheet = [dict(zip(cols, l.rstrip("\n").split("\t"))) for l in fh if l.strip()]
    mats, genesets = [], []
    for r in sheet:
        pre = os.path.join(args.raw, r["prefix"])
        X, bc, feats = read_10x_h5(pre + "_cell_feature_matrix.h5")
        keep = set(read_parquet(pre + "_cells.parquet.gz").column("cell_id").to_pylist())
        cls = feature_classes(feats, None)[0]
        g = [feats["name"][i] for i in np.where(cls == "gene")[0]]
        idx = [i for i, b in enumerate(bc) if b in keep]
        mats.append((r["sample"], X[idx], [bc[i] for i in idx], feats["name"]))
        genesets.append(set(g))
        print(f"{r['sample']}: {len(idx)} cells, {len(g)} genes")
    common = sorted(set.intersection(*genesets))
    union = set.union(*genesets)
    print(f"genes in every section: {len(common)}; in some sections only: {len(union) - len(common)} "
          f"({', '.join(sorted(union - set(common))[:20])}{' ...' if len(union) - len(common) > 20 else ''})")

    blocks, samples, cells = [], [], []
    for s, X, bc, names in mats:
        pos = {n: i for i, n in enumerate(names)}
        B = X[:, [pos[g] for g in common]].astype(np.float32).tocsr()
        tot = np.asarray(B.sum(axis=1)).ravel()
        ok = np.where(tot > 0)[0]
        blocks.append(B[ok]); samples += [s] * len(ok); cells += [bc[i] for i in ok]
        print(f"  {s}: {len(ok)} of {len(bc)} cells with gene counts")
    a = ad.AnnData(sparse.vstack(blocks).tocsr())
    a.var_names = common
    a.obs_names = [f"{s}:{c}" for s, c in zip(samples, cells)]
    a.obs["sample"] = samples
    print(f"joint matrix: {a.n_obs} cells x {a.n_vars} genes")
    sc.pp.normalize_total(a, target_sum=1e4)
    sc.pp.log1p(a)
    a.layers["lognorm"] = a.X.copy()
    sc.pp.scale(a, max_value=10)
    n_pcs = min(30, a.n_vars - 1)
    sc.tl.pca(a, n_comps=n_pcs, random_state=args.seed)
    Z = np.asarray(a.X)
    sc.pp.neighbors(a, n_neighbors=20, n_pcs=n_pcs, random_state=args.seed)
    scan = []
    for res in [float(x) for x in args.resolutions.split(",")]:
        key = f"leiden_{res}"
        sc.tl.leiden(a, resolution=res, flavor="igraph", n_iterations=2, random_state=args.seed, key_added=key)
        k = a.obs[key].nunique()
        scan.append([res, k])
        print(f"  resolution {res}: {k} clusters ({time.time() - t0:.0f} s)")
    write_tsv(os.path.join(args.out, "resolution_scan.tsv"), ["resolution", "n_clusters"], scan)
    best = min(scan, key=lambda r: (abs(r[1] - args.target), r[0]))
    key = f"leiden_{best[0]}"
    print(f"kept resolution {best[0]}: {best[1]} clusters (target {args.target})")
    clus = a.obs[key].astype(str).values

    vn = list(a.var_names)
    used = {lin: [g for g in genes if g in vn] for lin, genes in LINEAGES.items()}
    used = {k: v for k, v in used.items() if len(v) >= 2}
    for lin, genes in LINEAGES.items():
        print(f"   markers {lin:<11} in panel: {','.join(x for x in genes if x in vn) or '-'}"
              + ("" if lin in used else "  (fewer than 2: lineage not scored)"))
    lins = list(used)
    S = np.c_[[Z[:, [vn.index(x) for x in used[l]]].mean(axis=1) for l in lins]].T
    cl_ids = sorted(set(clus), key=int)
    sample_ids = [r["sample"] for r in sheet]
    samp = np.array(samples)
    rows, lab = [], []
    print("   cluster  n_cells  proposed     " + "  ".join(f"{l[:6]:>6}" for l in lins) + "  top genes")
    for c in cl_ids:
        m = clus == c
        sm = S[m].mean(axis=0)
        prop = lins[int(np.argmax(sm))] if sm.max() > 0 else "unassigned"
        top = [vn[i] for i in np.argsort(-Z[m].mean(axis=0))[:12]]
        per = [int((m & (samp == s)).sum()) for s in sample_ids]
        rows.append([c, int(m.sum()), prop] + [float(v) for v in sm] + [",".join(top)] + per)
        lab.append([c, prop])
        print(f"   {c:>7}  {int(m.sum()):7d}  {prop:<11}  " + "  ".join(f"{v:6.2f}" for v in sm) + "  " + ", ".join(top))
    write_tsv(os.path.join(args.out, "cluster_summary.tsv"),
              ["cluster", "n_cells", "proposed_label"] + [f"mean_score_{l}" for l in lins] + ["top_genes"]
              + [f"n_{s}" for s in sample_ids], rows)
    write_tsv(os.path.join(args.out, "labels_proposed.tsv"), ["cluster", "label"], lab)
    write_tsv(os.path.join(args.out, "clusters.tsv"), ["sample", "cell_id", "cluster"],
              [[s, c, k] for s, c, k in zip(samples, cells, clus)])
    with open(os.path.join(args.out, "cluster_config.json"), "w") as fh:
        json.dump(dict(sheet=args.sheet, n_cells=int(a.n_obs), n_genes=len(common), resolution=best[0],
                       n_clusters=int(best[1]), target=args.target, scan=scan, n_pcs=n_pcs, n_neighbors=20,
                       seed=args.seed, lineage_markers_used=used, scanpy=sc.__version__,
                       created=time.strftime("%Y-%m-%dT%H:%M:%S")), fh, indent=1)
    print(f"done in {time.time() - t0:.0f} s -> {args.out}")


if __name__ == "__main__":
    main()
