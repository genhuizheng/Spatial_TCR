#!/usr/bin/env python3
"""TCR-centred concentric shells for one Xenium section (GSE300147, McCord et al. 2026).

Inputs (Xenium outputs as deposited on GEO): <prefix>_cells.parquet.gz (centroids in um) and
<prefix>_cell_feature_matrix.h5 (Xenium's own transcript-to-cell assignment, used unchanged).

TCR calls. TCR probes are Gene Expression features named <probe_group>_<CDR3aa>_<chain>; the
section's own patient has probe_group == --probe-group, the other groups are other patients'
probes and serve as negative controls (McCord et al.). McCord et al. accepted a probe if it was
detected in at least five T cells and enriched in the T-cell cluster, and published no per-cell
count threshold. Here a probe passes if it is detected (count >= 1) in >= --min-cells cells; the
T-cell enrichment half of the rule needs cell annotations and is reported, not applied (see
tcr_probe_qc.tsv). A focal cell is any cell with >= 1 count of a passing own-patient probe. All
raw probe counts are kept; probe chains are never paired into alpha-beta clonotypes here.

Shells (each section on its own; no neighbour crosses sections):
  shell 0   the focal cell itself, always a separate row
  physical  shell k (k >= 1) = other cells whose centroid lies in ((k-1)w, kw] um of the focal
            centroid (a cell at distance 0 goes to shell 1). w defaults to the section's median
            Delaunay edge length, the typical centroid spacing of adjacent cells (one cell layer;
            the median nearest-neighbour distance is a minimum and left shell 1 mostly empty);
            shells run out to --max-radius. Fine rings add up, so coarser radius sets are sums
            of rings.
  graph     shell k = cells exactly k hops from the focal cell in the Delaunay triangulation of
            the centroids (squidpy's delaunay=True graph; qhull option QJ so duplicate centroids
            keep their edges), up to --max-hops; --max-edge prunes long edges (default: none).

Per scheme the outputs are shells_<scheme>.h5 (CSR rows x features: raw = summed raw counts,
lognorm = log1p(raw / gene total x 1e4), gene total = counts of non-TCR, non-control features)
and shells_<scheme>_rows.tsv (one row per focal cell and shell, with cell counts, distances,
coverage and TCR neighbour counts). The three shell-0 views (shell0_only, outer_only,
shell0_plus_outer) are row selections of the same files, see xenium_shell_views.py.
"""
import argparse
import gzip
import io
import json
import os
import platform
import re
import sys
import time

import h5py
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import scipy
from scipy import sparse
from scipy.spatial import Delaunay, cKDTree

PROBE_RE = re.compile(r"^([0-9A-Za-z]+)_([A-Z]+)_(TR[ABGD])$")
T_MARKERS = ["CD3D", "CD3E", "CD3G", "CD2", "CD247"]


def read_parquet(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rb") as fh:
            return pq.read_table(pa.BufferReader(fh.read()))
    return pq.read_table(path)


def read_10x_h5(path):
    with h5py.File(path, "r") as f:
        m = f["matrix"]
        shape = tuple(int(x) for x in m["shape"][:])
        X = sparse.csc_matrix((m["data"][:], m["indices"][:], m["indptr"][:]), shape=shape)
        barcodes = [b.decode() for b in m["barcodes"][:]]
        feats = {k: [b.decode() for b in m["features"][k][:]] for k in ("id", "name", "feature_type")}
    return X.T.tocsr().astype(np.int64), barcodes, feats


def feature_classes(feats, group):
    cls, chain, cdr3, pgroup = [], [], [], []
    for name, ftype in zip(feats["name"], feats["feature_type"]):
        m = PROBE_RE.match(name)
        if ftype != "Gene Expression":
            cls.append("control"); chain.append(""); cdr3.append(""); pgroup.append("")
        elif m:
            cls.append("tcr_own" if m.group(1) == group else "tcr_other")
            pgroup.append(m.group(1)); cdr3.append(m.group(2)); chain.append(m.group(3))
        else:
            cls.append("gene"); chain.append(""); cdr3.append(""); pgroup.append("")
    return np.array(cls), chain, cdr3, pgroup


def write_tsv(path, header, rows):
    with open(path, "w") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join("" if v is None else (f"{v:.4g}" if isinstance(v, float) else str(v)) for v in r) + "\n")


def write_csr(h5, name, M):
    g = h5.create_group(name)
    g.create_dataset("data", data=M.data, compression="gzip")
    g.create_dataset("indices", data=M.indices.astype(np.int32), compression="gzip")
    g.create_dataset("indptr", data=M.indptr.astype(np.int64))
    g.create_dataset("shape", data=np.array(M.shape, dtype=np.int64))


def delaunay_adjacency(xy, max_edge):
    tri = Delaunay(xy, qhull_options="QJ")
    s = tri.simplices
    e = np.vstack([s[:, [0, 1]], s[:, [1, 2]], s[:, [0, 2]]])
    e = np.unique(np.sort(e, axis=1), axis=0)
    length = np.linalg.norm(xy[e[:, 0]] - xy[e[:, 1]], axis=1)
    n_all = len(e)
    if max_edge:
        keep = length <= max_edge
        e, length = e[keep], length[keep]
    n = len(xy)
    A = sparse.coo_matrix((np.ones(len(e) * 2), (np.r_[e[:, 0], e[:, 1]], np.r_[e[:, 1], e[:, 0]])), shape=(n, n)).tocsr()
    return A, length, n_all


def physical_members(tree, xy, focal, width, K):
    """(row, cell) pairs and distances for shells 1..K of each focal cell."""
    rows, cells, dists = [], [], []
    hits = tree.query_ball_point(xy[focal], r=K * width)
    for i, (f, idx) in enumerate(zip(focal, hits)):
        idx = np.asarray(idx, dtype=np.int64)
        idx = idx[idx != f]
        d = np.linalg.norm(xy[idx] - xy[f], axis=1)
        s = np.maximum(np.ceil(d / width - 1e-9).astype(np.int64), 1)
        ok = s <= K
        rows.append(i * (K + 1) + s[ok]); cells.append(idx[ok]); dists.append(d[ok])
    return np.concatenate(rows), np.concatenate(cells), np.concatenate(dists)


def graph_members(adj, xy, focal, H):
    n = adj.shape[0]
    hop = np.full(n, -1, dtype=np.int32)
    rows, cells, dists = [], [], []
    for i, f in enumerate(focal):
        hop[f] = 0
        seen = [np.array([f])]
        frontier = np.array([f])
        for h in range(1, H + 1):
            nb = np.unique(adj[frontier].indices)
            nb = nb[hop[nb] < 0]
            if not len(nb):
                break
            hop[nb] = h
            rows.append(np.full(len(nb), i * (H + 1) + h)); cells.append(nb)
            dists.append(np.linalg.norm(xy[nb] - xy[f], axis=1))
            seen.append(nb); frontier = nb
        hop[np.concatenate(seen)] = -1
    if not rows:
        return np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0)
    return np.concatenate(rows), np.concatenate(cells), np.concatenate(dists)


def coverage(tree, xy, focal, width, K, occ, n_ang=72):
    """Fraction of points on each ring's mid-circle within occ um of a cell centroid (QC only)."""
    ang = np.linspace(0, 2 * np.pi, n_ang, endpoint=False)
    unit = np.c_[np.cos(ang), np.sin(ang)]
    out = np.zeros((len(focal), K + 1))
    for s in range(1, K + 1):
        r = (s - 0.5) * width
        pts = (xy[focal][:, None, :] + r * unit[None, :, :]).reshape(-1, 2)
        d, _ = tree.query(pts, distance_upper_bound=occ)
        out[:, s] = np.isfinite(d).reshape(len(focal), n_ang).mean(axis=1)
    out[:, 0] = 1.0
    return out


def build(focal, n_shell, members, X, gene_cols, tcr_cell, share):
    """Aggregate shells; members = (row, cell, dist) for shells >= 1."""
    r, c, d = members
    n_rows = len(focal) * n_shell
    r = np.r_[np.arange(len(focal)) * n_shell, r]
    c = np.r_[focal, c]
    d = np.r_[np.zeros(len(focal)), d]
    A = sparse.csr_matrix((np.ones(len(r)), (r, c)), shape=(n_rows, X.shape[0]))
    raw = (A @ X).tocsr()
    raw.data = raw.data.astype(np.int64)
    gene_total = np.asarray(raw[:, gene_cols].sum(axis=1)).ravel()
    scale = np.divide(1e4, gene_total, out=np.zeros(n_rows), where=gene_total > 0)
    lognorm = raw.astype(np.float64).multiply(scale[:, None]).tocsr()
    lognorm.data = np.log1p(lognorm.data).astype(np.float32)
    lognorm.sort_indices(); raw.sort_indices()
    n_cells = np.bincount(r, minlength=n_rows)
    tot = np.asarray(X.sum(axis=1)).ravel()
    n_nonzero = np.bincount(r, weights=(tot[c] > 0), minlength=n_rows)
    n_tcr = np.bincount(r, weights=tcr_cell[c], minlength=n_rows)
    fidx = r // n_shell
    same = np.bincount(r, weights=share(fidx, c), minlength=n_rows)
    order = np.argsort(r, kind="stable")
    rs, ds = r[order], d[order]
    bounds = np.searchsorted(rs, np.arange(n_rows + 1))
    dmed = np.array([np.median(ds[bounds[i]:bounds[i + 1]]) if bounds[i + 1] > bounds[i] else np.nan for i in range(n_rows)])
    dmax = np.array([ds[bounds[i]:bounds[i + 1]].max() if bounds[i + 1] > bounds[i] else np.nan for i in range(n_rows)])
    return raw, lognorm, dict(n_cells=n_cells, n_nonzero=n_nonzero.astype(int), gene_total=gene_total.astype(int),
                              n_tcr=n_tcr.astype(int), same=same.astype(int), dmed=dmed, dmax=dmax)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", required=True)
    ap.add_argument("--prefix", required=True, help="path prefix of the Xenium files, e.g. data/raw/GSE300147/GSM9054481_Sept_11_24_240103")
    ap.add_argument("--probe-group", required=True, help="this patient's TCR probe group, e.g. 240103")
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-cells", type=int, default=5, help="probe passes if detected in >= this many cells (McCord: 5 T cells)")
    ap.add_argument("--width", default="auto", help="physical ring width in um, or auto = median Delaunay edge length")
    ap.add_argument("--max-radius", type=float, default=250.0, help="outer edge of the last physical ring, um")
    ap.add_argument("--max-hops", type=int, default=25)
    ap.add_argument("--max-edge", type=float, default=None, help="drop Delaunay edges longer than this (um); default keep all")
    ap.add_argument("--calls", default=None, help="output folder of xenium_tcr_calls.py: use its McCord-rule probes and "
                    "T-cluster focal cells (tier_mccord) instead of the --min-cells rule; rows get focal_strict")
    args = ap.parse_args()
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)

    X, barcodes, feats = read_10x_h5(args.prefix + "_cell_feature_matrix.h5")
    cells = read_parquet(args.prefix + "_cells.parquet.gz").to_pydict()
    pos = {cid: i for i, cid in enumerate(cells["cell_id"])}
    in_both = [i for i, b in enumerate(barcodes) if b in pos]
    print(f"{args.sample}: matrix {X.shape[0]} cells x {X.shape[1]} features; cells.parquet {len(pos)} cells; "
          f"in both {len(in_both)}; matrix only {X.shape[0] - len(in_both)}; parquet only {len(pos) - len(in_both)}")
    if len(in_both) < X.shape[0]:
        X = X[in_both]; barcodes = [barcodes[i] for i in in_both]
    j = np.array([pos[b] for b in barcodes])
    xy = np.c_[np.asarray(cells["x_centroid"], float)[j], np.asarray(cells["y_centroid"], float)[j]]
    n = len(barcodes)

    cls, chain, cdr3, pgroup = feature_classes(feats, args.probe_group)
    gene_cols = np.where(cls == "gene")[0]
    own = np.where(cls == "tcr_own")[0]
    other = np.where(cls == "tcr_other")[0]
    print(f"features: {len(gene_cols)} genes, {len(own)} own TCR probes (group {args.probe_group}), "
          f"{len(other)} other-patient TCR probes, {int((cls == 'control').sum())} controls")
    if not len(own):
        sys.exit(f"no TCR probes of group {args.probe_group}: wrong --probe-group?")

    # probe QC, with a descriptive T-cell marker check (not a filter)
    Xc = X.tocsc()
    det = (Xc > 0)
    n_det = np.asarray(det.sum(axis=0)).ravel()
    markers = [m for m in T_MARKERS if m in feats["name"]]
    tmark = np.zeros(n, bool)
    for m in markers:
        tmark |= np.asarray(Xc[:, feats["name"].index(m)].todense()).ravel() > 0
    passing = np.array([k for k in own if n_det[k] >= args.min_cells], dtype=int)
    qc = []
    for k in np.r_[own, other]:
        hit = det[:, k].nonzero()[0]
        qc.append([feats["name"][k], pgroup[k], cls[k], chain[k], cdr3[k], int(n_det[k]), int(Xc[:, k].sum()),
                   "yes" if (cls[k] == "tcr_own" and n_det[k] >= args.min_cells) else "no",
                   float(tmark[hit].mean()) if len(hit) else None])
    write_tsv(os.path.join(args.out, "tcr_probe_qc.tsv"),
              ["probe", "probe_group", "class", "chain", "cdr3_aa", "n_cells", "counts", "passes_min_cells",
               "frac_cells_with_T_marker"], qc)
    other_cells = int((np.asarray(Xc[:, other].sum(axis=1)).ravel() > 0).sum()) if len(other) else 0
    print(f"own probes detected in >= {args.min_cells} cells: {len(passing)} of {len(own)}; cells with any "
          f"other-patient probe count (negative control): {other_cells}; T markers used for the descriptor: {markers} "
          f"({tmark.mean():.1%} of all cells)")

    strict_cells = set()
    if args.calls:
        def tsv(name):
            with open(os.path.join(args.calls, name)) as fh:
                cols = fh.readline().rstrip("\n").split("\t")
                return [dict(zip(cols, l.rstrip("\n").split("\t"))) for l in fh]
        ok = {r["probe"] for r in tsv("probe_calls.tsv") if r["class"] == "tcr_own" and r["mccord_pass"] == "yes"}
        passing = np.array([k for k in own if feats["name"][k] in ok], dtype=int)
        cc = tsv("cell_calls.tsv")
        mccord_cells = {r["cell_id"] for r in cc if r["tier_mccord"] == "yes"}
        strict_cells = {r["cell_id"] for r in cc if r["tier_strict"] == "yes"}
        print(f"--calls {args.calls}: {len(passing)} own probes pass the McCord rule; focal cells tier_mccord "
              f"{len(mccord_cells)}, tier_strict {len(strict_cells)}")
    P = (X[:, passing] > 0).astype(np.int8).tocsr()
    tcr_cell = np.asarray(P.sum(axis=1)).ravel() > 0
    if args.calls:
        tcr_cell &= np.array([b in mccord_cells for b in barcodes])
        P = sparse.csr_matrix(P.multiply(tcr_cell[:, None]))
        P.eliminate_zeros()
    focal = np.where(tcr_cell)[0]
    if not len(focal):
        sys.exit("no focal TCR cells")
    obs = []
    Xr = X.tocsr()
    passing_set = set(passing.tolist())
    for k in own:
        for ci in Xc[:, k].nonzero()[0]:
            obs.append([args.sample, barcodes[ci], float(xy[ci, 0]), float(xy[ci, 1]), feats["name"][k], chain[k],
                        cdr3[k], int(Xc[ci, k]), "yes" if k in passing_set else "no",
                        int(P[ci].sum()), int(Xr[ci, gene_cols].sum())])
    write_tsv(os.path.join(args.out, "tcr_observations.tsv"),
              ["sample", "cell_id", "x_um", "y_um", "probe", "chain", "cdr3_aa", "count", "probe_passes",
               "n_passing_probes_in_cell", "cell_gene_counts"], obs)
    chains = {c: int((np.asarray(P[:, [i for i, k in enumerate(passing) if chain[k] == c]].sum(axis=1)).ravel() > 0).sum())
              for c in sorted({chain[k] for k in passing})}
    print(f"focal TCR cells: {len(focal)} ({len(focal) / n:.2%} of cells); by chain {chains}; "
          f"cells with > 1 passing probe: {int((np.asarray(P.sum(axis=1)).ravel() > 1).sum())}")

    # cells sharing a probe (same chain-level clone) with each focal cell
    S = (P @ P[focal].T).tocsc()

    def share(fidx, c):
        out = np.zeros(len(c))
        order = np.argsort(fidx, kind="stable")
        fs = fidx[order]
        b = np.searchsorted(fs, np.arange(len(focal) + 1))
        for i in range(len(focal)):
            sel = order[b[i]:b[i + 1]]
            col = S.indices[S.indptr[i]:S.indptr[i + 1]]
            out[sel] = np.isin(c[sel], col)
        return out

    feat_rows = [[i, feats["id"][i], feats["name"][i], feats["feature_type"][i], cls[i]] for i in range(len(cls))]
    write_tsv(os.path.join(args.out, "features.tsv"), ["col", "id", "name", "feature_type", "class"], feat_rows)

    adj, elen, n_edges_all = delaunay_adjacency(xy, args.max_edge)
    med_edge = float(np.median(elen))
    print(f"Delaunay graph: {n_edges_all} edges, kept {len(elen)}; edge length median {med_edge:.2f} um, "
          f"p99 {np.quantile(elen, 0.99):.2f} um, max {elen.max():.1f} um; edges > 3x median: {int((elen > 3 * med_edge).sum())}")

    tree = cKDTree(xy)
    nn = tree.query(xy, k=2)[0][:, 1]
    width = med_edge if args.width == "auto" else float(args.width)
    K = int(np.floor(args.max_radius / width + 1e-9))
    occ = float(np.quantile(nn, 0.99))
    print(f"nearest-neighbour centroid distance: median {np.median(nn):.2f} um, p99 {occ:.2f} um (coverage radius); "
          f"physical ring width {width:.2f} um, {K} rings to {K * width:.1f} um")

    cov = coverage(tree, xy, focal, width, K, occ)
    schemes = {
        "physical": (K + 1, physical_members(tree, xy, focal, width, K)),
        "graph": (args.max_hops + 1, graph_members(adj, xy, focal, args.max_hops)),
    }
    for scheme, (n_shell, members) in schemes.items():
        raw, lognorm, st = build(focal, n_shell, members, X, gene_cols, tcr_cell.astype(float), share)
        with h5py.File(os.path.join(args.out, f"shells_{scheme}.h5"), "w") as h5:
            write_csr(h5, "raw", raw)
            write_csr(h5, "lognorm", lognorm)
        rows = []
        for i in range(raw.shape[0]):
            f, s = divmod(i, n_shell)
            ci = focal[f]
            if scheme == "physical":
                ri, ro = (0.0, 0.0) if s == 0 else ((s - 1) * width, s * width)
                area = None if s == 0 else float(np.pi * (ro ** 2 - ri ** 2))
                geo = [ri, ro, area, float(cov[f, s])]
            else:
                geo = [None, None, None, None]
            n_c = int(st["n_cells"][i])
            rows.append([args.sample, barcodes[ci], "yes" if barcodes[ci] in strict_cells else "no", s, scheme] + geo +
                        [n_c, int(st["n_nonzero"][i]), int(st["gene_total"][i]),
                         None if np.isnan(st["dmed"][i]) else float(st["dmed"][i]),
                         None if np.isnan(st["dmax"][i]) else float(st["dmax"][i]),
                         int(st["n_tcr"][i]) - (1 if s == 0 else 0), int(st["same"][i]) - (1 if s == 0 else 0)])
        write_tsv(os.path.join(args.out, f"shells_{scheme}_rows.tsv"),
                  ["sample", "focal_cell_id", "focal_strict", "shell", "scheme", "r_inner_um", "r_outer_um", "area_um2", "coverage",
                   "n_cells", "n_cells_with_counts", "gene_counts", "dist_median_um", "dist_max_um",
                   "n_tcr_cells", "n_same_probe_cells"], rows)
        nc = st["n_cells"].reshape(len(focal), n_shell)
        empty = (nc == 0).sum(axis=0)
        print(f"== {scheme}: {raw.shape[0]} rows ({len(focal)} focal x {n_shell} shells incl. shell 0), "
              f"raw nnz {raw.nnz}")
        print("   shell  median_cells  focal_with_0_cells  median_dist_um" + ("  median_coverage" if scheme == "physical" else ""))
        dm = st["dmed"].reshape(len(focal), n_shell)
        for s in range(n_shell):
            line = f"   {s:5d}  {np.median(nc[:, s]):12.0f}  {empty[s]:18d}  {np.nanmedian(dm[:, s]) if np.isfinite(dm[:, s]).any() else float('nan'):14.1f}"
            if scheme == "physical":
                line += f"  {np.median(cov[:, s]):15.2f}"
            print(line)

    cfg = dict(sample=args.sample, prefix=args.prefix, probe_group=args.probe_group, min_cells=args.min_cells, calls=args.calls,
               width_um=width, width_rule=args.width, n_physical_rings=K, max_radius_um=args.max_radius,
               max_hops=args.max_hops, max_edge_um=args.max_edge, coverage_occupancy_um=occ,
               n_cells=n, n_focal=int(len(focal)), passing_probes=[feats["name"][k] for k in passing],
               t_markers=markers, python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               h5py=h5py.__version__, pyarrow=pa.__version__, created=time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(os.path.join(args.out, "config.json"), "w") as fh:
        json.dump(cfg, fh, indent=1)
    print(f"{args.sample}: done in {time.time() - t0:.0f} s -> {args.out}")


if __name__ == "__main__":
    main()
