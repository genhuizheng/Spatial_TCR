#!/usr/bin/env python3
"""Read the shell tables written by xenium_shells.py in one of the three shell-0 views.

  shell0_only        shell 0 rows only (the focal TCR cell's own counts)
  outer_only         shells >= 1 only (neighbours; the focal cell is never in these rows)
  shell0_plus_outer  all rows, shell 0 kept as its own row (never summed into an outer shell)

--merge E1,E2,...  sums fine outer shells into coarser ones before the view is taken: for the
physical scheme the edges are radii in um (e.g. 25,75,150 gives (0,25], (25,75], (75,150]); a
fine ring goes to the coarse shell that holds its midpoint, so the effective edges are the ring
edges nearest to E (reported as r_inner_um / r_outer_um); rings beyond the last edge are dropped.
For the graph scheme the edges are hop numbers (e.g. 1,3,6).
--pool-outer sums all outer shells of a focal cell into one row. --strict keeps only focal cells
of the strict tier (focal_strict == yes, from xenium_shells.py --calls). lognorm is recomputed from the
summed raw counts the same way as in xenium_shells.py.

As a library: rows, raw, lognorm = load(dir, scheme, view, merge=None, pool_outer=False)
As a script it prints a summary of each view and checks that shell0_only + outer_only add up
to shell0_plus_outer.
"""
import argparse
import os
import sys

import h5py
import numpy as np
from scipy import sparse

VIEWS = ("shell0_only", "outer_only", "shell0_plus_outer")


def read_rows(path):
    with open(path) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        rows = [dict(zip(cols, line.rstrip("\n").split("\t"))) for line in fh]
    for r in rows:
        r["shell"] = int(r["shell"])
    return rows


def read_csr(h5, name):
    g = h5[name]
    return sparse.csr_matrix((g["data"][:], g["indices"][:], g["indptr"][:]), shape=tuple(g["shape"][:]))


def lognorm_of(raw, gene_cols):
    tot = np.asarray(raw[:, gene_cols].sum(axis=1)).ravel()
    scale = np.divide(1e4, tot, out=np.zeros(raw.shape[0]), where=tot > 0)
    ln = raw.astype(np.float64).multiply(scale[:, None]).tocsr()
    ln.data = np.log1p(ln.data).astype(np.float32)
    return ln


def gene_columns(d):
    with open(os.path.join(d, "features.tsv")) as fh:
        fh.readline()
        return np.array([int(l.split("\t")[0]) for l in fh if l.rstrip("\n").split("\t")[4] == "gene"])


def load(d, scheme, view, merge=None, pool_outer=False, strict=False):
    if view not in VIEWS:
        raise ValueError(f"view must be one of {VIEWS}")
    rows = read_rows(os.path.join(d, f"shells_{scheme}_rows.tsv"))
    with h5py.File(os.path.join(d, f"shells_{scheme}.h5"), "r") as h5:
        raw = read_csr(h5, "raw")
        lognorm = read_csr(h5, "lognorm")
    if strict:
        sel = [i for i, r in enumerate(rows) if r.get("focal_strict") == "yes"]
        rows, raw, lognorm = [rows[i] for i in sel], raw[sel], lognorm[sel]
    if merge or pool_outer:
        group = []
        for r in rows:
            s = r["shell"]
            if s == 0:
                g = 0
            elif pool_outer:
                g = 1
            else:
                key = s if scheme == "graph" else (float(r["r_inner_um"]) + float(r["r_outer_um"])) / 2
                g = next((i + 1 for i, e in enumerate(merge) if key <= e + 1e-6), None)
            group.append(g)
        keys, new_rows, src = {}, [], []
        for i, (r, g) in enumerate(zip(rows, group)):
            if g is None:
                continue
            k = (r["sample"], r["focal_cell_id"], g)
            if k not in keys:
                keys[k] = len(new_rows)
                new_rows.append({"sample": r["sample"], "focal_cell_id": r["focal_cell_id"], "shell": g,
                                 "scheme": scheme, "n_cells": 0, "n_tcr_cells": 0, "n_same_probe_cells": 0,
                                 "fine_shells": [], "r_inner_um": r.get("r_inner_um", ""), "r_outer_um": ""})
            nr = new_rows[keys[k]]
            nr["r_outer_um"] = r.get("r_outer_um", "")
            for c in ("n_cells", "n_tcr_cells", "n_same_probe_cells"):
                nr[c] += int(r[c])
            nr["fine_shells"].append(r["shell"])
            src.append((keys[k], i))
        M = sparse.csr_matrix((np.ones(len(src)), ([a for a, _ in src], [b for _, b in src])), shape=(len(new_rows), len(rows)))
        raw = (M @ raw).tocsr()
        raw.data = raw.data.astype(np.int64)
        lognorm = lognorm_of(raw, gene_columns(d))
        rows = new_rows
    keep = [i for i, r in enumerate(rows) if (view == "shell0_plus_outer") or (view == "shell0_only") == (r["shell"] == 0)]
    return [rows[i] for i in keep], raw[keep], lognorm[keep]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="one sample's output folder from xenium_shells.py")
    ap.add_argument("--scheme", choices=("physical", "graph"), default="physical")
    ap.add_argument("--merge", default=None)
    ap.add_argument("--pool-outer", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    merge = [float(x) if args.scheme == "physical" else int(x) for x in args.merge.split(",")] if args.merge else None

    res = {v: load(args.dir, args.scheme, v, merge, args.pool_outer, args.strict) for v in VIEWS}
    if not res["shell0_plus_outer"][0]:
        print(f"{args.scheme}: no rows" + (" with focal_strict == yes" if args.strict else ""))
        sys.exit(0)
    for v, (rows, raw, ln) in res.items():
        shells = sorted({r["shell"] for r in rows})
        print(f"{args.scheme} {v}: {len(rows)} rows, shells {shells[0]}..{shells[-1]} ({len(shells)}), "
              f"raw counts {int(raw.sum())}, cells {sum(int(r['n_cells']) for r in rows)}")
        if v == "shell0_plus_outer" and args.scheme == "physical":
            edges = sorted({(r["shell"], r["r_inner_um"], r["r_outer_um"]) for r in rows})
            print("   shell edges (um): " + ", ".join(f"{s}: ({a}, {b}]" for s, a, b in edges))
    s0, out, both = (int(res[v][1].sum()) for v in VIEWS)
    c0 = sum(int(r["n_cells"]) for r in res["shell0_only"][0])
    n_focal = len({(r["sample"], r["focal_cell_id"]) for r in res["shell0_only"][0]})
    ok = s0 + out == both and c0 == n_focal and all(r["shell"] > 0 for r in res["outer_only"][0])
    print(f"check: shell0 {s0} + outer {out} = {s0 + out} vs shell0_plus_outer {both}; shell-0 rows hold "
          f"{c0} cells for {n_focal} focal cells -> {'OK' if ok else 'FAILED'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
