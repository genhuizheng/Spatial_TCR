#!/bin/bash
# Link the brain metastasis Visium TRB spot calls (visium_tcr.slurm) to the matched 10x single-cell
# clonotypes (sctcr_mixcr.slurm). Small tables only: fine on the login node.
#   bash scripts/link_bm_sctcr.sh
# Outputs: outputs/sctcr_link/{clonotypes_<sample>.tsv, clone_links.tsv, spot_links.tsv, link_summary.tsv}

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
PY=${PY:-python3}
cd "$ROOT" || exit 1
OUT=outputs/sctcr_link
mkdir -p "$OUT"

SC=""
for s in $(awk -F'\t' 'NR > 1 { print $1 }' metadata/bm_sctcr_samples.tsv); do
    D=outputs/sctcr_mixcr/$s
    [ -f "$D/DONE" ] || { echo "$s: no finished MiXCR output, skipped"; continue; }
    $PY scripts/mixcr_sc_clonotypes.py --sample "$s" --clones "$D/result.clones.tsv" \
        --groups "$D/result.clone.groups_TRAB.tsv" --out "$OUT/clonotypes_$s.tsv" || continue
    SC="$SC $OUT/clonotypes_$s.tsv"
done

SPOTS=""
for p in 15 16 19 24 26 27; do
    f=outputs/visium_tcr/pt$p/spot_clone_long.tsv
    [ -s "$f" ] && SPOTS="$SPOTS $p=$f" || echo "pt$p: no Visium spot table, skipped"
done
[ -n "$SC" ] && [ -n "$SPOTS" ] || { echo "nothing to link"; exit 1; }

echo "== link (TRB CDR3 nt; in-tissue spots)"
$PY scripts/link_spot_sctcr.py --spots $SPOTS --sc $SC --out "$OUT" > "$OUT/link_summary.log" || exit 1
column -t -s $'\t' "$OUT/link_summary.tsv"
echo "== expected-pair links per patient (nt, attributed)"
awk -F'\t' 'NR > 1 && $9 == "expected" && $10 == "nt" { n[$1 "\t" $7]++; if ($19 == "yes") a[$1 "\t" $7]++; if ($14 == "yes") v[$1 "\t" $7]++ }
            END { for (k in n) print k "\t" n[k] "\t" a[k] + 0 "\t" v[k] + 0 }' "$OUT/clone_links.tsv" \
    | sort | (printf 'patient\tsc_sample\tlinks\tattributed\tV_agrees\n'; cat) | column -t -s $'\t'
echo "== spots with a paired TRA: $(awk -F'\t' 'NR > 1 && $13 != "" { print $1 "\t" $2 }' "$OUT/spot_links.tsv" | sort -u | wc -l)"
