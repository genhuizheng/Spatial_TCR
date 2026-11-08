#!/usr/bin/env python3
"""Compare the Xenium TCR probe calls of all GSE300147 sections with McCord et al. 2026.

Reads <run>/<sample>/calls/{probe_calls.tsv, cell_calls.tsv, calls_config.json} written by
xenium_tcr_calls.py for every section in --sheet, and reports the published headline numbers:
  - "70 TCR-targeting probes" designed, "61 validated probes present in over 2,000 T cells in eight
    patients" (a probe is validated if it passes the McCord rule in a section of its own patient);
  - "Six of seven samples yielded successful TCR probes in both runs" (patients with two runs);
  - "Most probes were specifically detected in T cells from the corresponding patient tissue but
    not in mismatched samples": every probe is also tested with the same rule in the sections of
    other patients whose panel carries it (mismatched tissue), which counts false passes.
T cells with a validated probe = T-cluster cells with >= 1 count of an own probe that passes the
rule in that section (tier_mccord), summed over sections; the strict tier is reported alongside.
Outputs in --out: probe_validation.tsv, section_summary.tsv, summary.json.
"""
import argparse
import json
import os
from collections import defaultdict


def tsv(path):
    with open(path) as fh:
        cols = fh.readline().rstrip("\n").split("\t")
        return [dict(zip(cols, l.rstrip("\n").split("\t"))) for l in fh if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="run folder holding <sample>/calls/")
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    sheet = tsv(args.sheet)

    group_patient, sections, probes = {}, [], defaultdict(list)
    for r in sheet:
        d = os.path.join(args.run, r["sample"], "calls")
        if not os.path.exists(os.path.join(d, "probe_calls.tsv")):
            print(f"{r['sample']}: no calls, skipped")
            continue
        cfg = json.load(open(os.path.join(d, "calls_config.json")))
        g = cfg.get("probe_group")
        if g:
            if group_patient.get(g, r["patient"]) != r["patient"]:
                print(f"WARNING: probe group {g} maps to patients {group_patient[g]} and {r['patient']}")
            group_patient[g] = r["patient"]
        cells = tsv(os.path.join(d, "cell_calls.tsv"))
        pc = tsv(os.path.join(d, "probe_calls.tsv"))
        own = [p for p in pc if p["class"] == "tcr_own"]
        sections.append(dict(sample=r["sample"], patient=r["patient"], run=r["run"], group=g or "",
                             n_own_probes=len(own), n_own_pass=sum(p["mccord_pass"] == "yes" for p in own),
                             n_own_strict=sum(p["strict_pass"] == "yes" for p in own),
                             t_cells_mccord=sum(c["tier_mccord"] == "yes" for c in cells),
                             t_cells_strict=sum(c["tier_strict"] == "yes" for c in cells)))
        for p in pc:
            probes[p["probe"]].append(dict(p, sample=r["sample"], patient=r["patient"]))

    rows = []
    for name, recs in sorted(probes.items()):
        g = recs[0]["probe_group"]
        pat = group_patient.get(g, "")
        own = [x for x in recs if x["patient"] == pat]
        mis = [x for x in recs if x["patient"] != pat]
        rows.append(dict(probe=name, chain=recs[0]["chain"], probe_group=g, patient=pat or "no section",
                         own_sections=len(own), own_pass=sum(x["mccord_pass"] == "yes" for x in own),
                         own_strict=sum(x["strict_pass"] == "yes" for x in own),
                         own_T_cells=sum(int(x["n_T_cells"]) for x in own),
                         mismatched_sections=len(mis), mismatched_pass=sum(x["mccord_pass"] == "yes" for x in mis),
                         mismatched_T_cells=sum(int(x["n_T_cells"]) for x in mis),
                         max_mismatched_T_rate=max((float(x["T_detection_rate"]) for x in mis), default=0.0),
                         max_own_T_rate=max((float(x["T_detection_rate"]) for x in own), default=0.0)))
    cols = list(rows[0]) if rows else []
    with open(os.path.join(args.out, "probe_validation.tsv"), "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")
    scols = list(sections[0]) if sections else []
    with open(os.path.join(args.out, "section_summary.tsv"), "w") as fh:
        fh.write("\t".join(scols) + "\n")
        for r in sections:
            fh.write("\t".join(str(r[c]) for c in scols) + "\n")

    with_section = [r for r in rows if r["own_sections"]]
    validated = [r for r in with_section if r["own_pass"]]
    strict = [r for r in with_section if r["own_strict"]]
    pats_val = sorted({r["patient"] for r in validated}, key=int)
    by_pat = defaultdict(list)
    for s in sections:
        by_pat[s["patient"]].append(s)
    dup = {p: v for p, v in by_pat.items() if len(v) >= 2}
    dup_ok = sorted((p for p, v in dup.items() if all(s["n_own_pass"] > 0 for s in v)), key=int)
    t_m = sum(s["t_cells_mccord"] for s in sections)
    t_s = sum(s["t_cells_strict"] for s in sections)
    mis_pairs = sum(r["mismatched_sections"] for r in rows)
    mis_pass = sum(r["mismatched_pass"] for r in rows)
    print("== sections")
    print("   sample     patient run group      own_probes pass strict  T_cells_mccord T_cells_strict")
    for s in sections:
        print(f"   {s['sample']:<10} {s['patient']:>7} {s['run']:>3} {s['group']:<10} {s['n_own_probes']:10d} "
              f"{s['n_own_pass']:4d} {s['n_own_strict']:6d}  {s['t_cells_mccord']:14d} {s['t_cells_strict']:14d}")
    print("== McCord et al. vs this reproduction")
    print(f"   TCR probes designed:          paper 70  | here {len(rows)} on the panels, {len(with_section)} for patients with a section")
    for ch in ("TRA", "TRB"):
        print(f"     {ch}: {sum(r['chain'] == ch for r in with_section)} with a section, "
              f"{sum(r['chain'] == ch for r in validated)} validated, {sum(r['chain'] == ch for r in strict)} strict")
    print(f"   validated probes:             paper 61  | here {len(validated)} (strict tier {len(strict)})")
    print(f"   T cells with a valid probe:   paper >2,000 | here {t_m} (strict tier {t_s}), summed over sections")
    print(f"   patients with a valid probe:  paper 8   | here {len(pats_val)} ({', '.join(pats_val)})")
    print(f"   duplicate patients, success in both runs: paper 6 of 7 | here {len(dup_ok)} of {len(dup)} ({', '.join(dup_ok)})")
    print(f"   mismatched tissue: {mis_pass} of {mis_pairs} (probe, other-patient section) pairs pass the rule "
          f"({sum(r['mismatched_pass'] > 0 for r in validated)} of {len(validated)} validated probes pass somewhere mismatched)")
    json.dump(dict(probes_on_panels=len(rows), probes_with_section=len(with_section), validated=len(validated),
                   strict=len(strict), t_cells_mccord=t_m, t_cells_strict=t_s, patients_validated=pats_val,
                   duplicate_patients=sorted(dup, key=int), duplicate_success=dup_ok, mismatched_pairs=mis_pairs,
                   mismatched_pass=mis_pass, group_patient=group_patient),
              open(os.path.join(args.out, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
