#!/usr/bin/env python3
"""Compare two spot x clone TCR count matrices (visium_tcr_counts.py --matrix layout,
or the authors' output_counts.txt) at the level of (spot barcode, chain, CDR3 nt), so the
check does not depend on MiXCR numbering clones the same way in both runs.

Usage: compare_tcr_counts.py REF_MATRIX REF_CLONES TEST_MATRIX TEST_CLONES
Exit code 0 only if every (spot, chain, CDR3) UMI count is identical.
"""
import sys
from collections import defaultdict


def clone_keys(path):
    keys = {}
    with open(path) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        i_id, i_v, i_cdr3 = cols.index("cloneId"), cols.index("allVHitsWithScore"), cols.index("nSeqCDR3")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            keys[f[i_id]] = (f[i_v][:3], f[i_cdr3])
    return keys


def load(matrix, clones):
    keys = clone_keys(clones)
    agg = defaultdict(int)
    with open(matrix) as fh:
        cols = [c.replace("clone", "", 1) for c in fh.readline().rstrip("\n").rstrip("\t").split("\t")]
        for line in fh:
            f = line.rstrip("\n").split("\t")
            for c, v in zip(cols, f[1:1 + len(cols)]):
                if v and int(v):
                    agg[(f[0],) + keys[c]] += int(v)
    return agg, len(cols)


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    ref, nref = load(sys.argv[1], sys.argv[2])
    test, ntest = load(sys.argv[3], sys.argv[4])
    diff = [k for k in set(ref) | set(test) if ref.get(k, 0) != test.get(k, 0)]
    for name, d, n in (("reference", ref, nref), ("test", test, ntest)):
        trb = sum(v for k, v in d.items() if k[1] == "TRB")
        print(f"{name}: {n} clones, {sum(d.values())} UMIs ({trb} TRB) in {len(d)} spot-CDR3 cells")
    print(f"spot-CDR3 cells that differ: {len(diff)}")
    for k in sorted(diff)[:10]:
        print("   ", k, "reference", ref.get(k, 0), "test", test.get(k, 0))
    print("MATCH" if not diff else "MISMATCH")
    sys.exit(0 if not diff else 1)


if __name__ == "__main__":
    main()
