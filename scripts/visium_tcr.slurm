#!/bin/bash
#SBATCH -J visium_tcr
#SBATCH -p gg
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 04:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/visium_tcr_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/visium_tcr_%j.err

# Spot-level TCR calls for the brain metastasis Visium TCR data (GSE179572 + PRJNA742564),
# following Hudson and Sudmeier 2022 (github.com/whhudson/spatialTCR) exactly:
#   mixcr analyze shotgun on read 2 (MiXCR 3.0.13, authors' options)
#   mixcr exportReadsForClones -s
#   scripts/visium_tcr_counts.py (Python 3 port of their combine_counts.py)
# The first sample, TEST_pt16_downsample, is the authors' own 100k-read test set; its counts
# must match their published output_counts.txt (compare_tcr_counts.py), otherwise the real
# samples are not run (set FORCE=1 to override).
# Setup first, on the login node: bash scripts/setup_mixcr.sh
# SAMPLES="pt15 pt19" limits the run; finished samples (DONE file) are skipped.
# Outputs: outputs/visium_tcr/<sample>/{spot_clone_matrix.tsv, spot_clone_long.tsv, mixcr/}
#          outputs/visium_tcr/summary.tsv

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
TOOLS=${TOOLS:-/scratch/10119/ghzheng/tools}
MEM=${MEM:-48g}
cd "$ROOT" || exit 1
SHEET=metadata/visium_tcr_samples.tsv
JAR=$TOOLS/mixcr-3.0.13/mixcr.jar
[ -s "$JAR" ] || { echo "missing $JAR: run bash scripts/setup_mixcr.sh on the login node"; exit 1; }

if ! java -Xmx256m -version >/dev/null 2>&1; then
    module load java >/dev/null 2>&1 || module load jdk >/dev/null 2>&1
fi
java -Xmx256m -version >/dev/null 2>&1 || { echo "no working java"; exit 1; }
MIXCR="java -Xmx$MEM -jar $JAR"
PY=${PY:-python3}
echo "$(date) java: $(command -v java)  python: $($PY --version 2>&1)  MiXCR: $JAR"

SAMPLES=${SAMPLES:-$(awk -F'\t' 'NR > 1 { print $1 }' "$SHEET")}
OUT=$ROOT/outputs/visium_tcr
mkdir -p "$OUT"
SUM=$OUT/summary.tsv
[ -f "$SUM" ] || printf 'sample\tpatient\trun\tr2_reads\taligned_pct\tclonotypes\ttrb_clonotypes\tumis_on_spots\ttrb_umis_on_spots\ttrb_umis_in_tissue\tspots_with_trb\tin_tissue_spots_with_trb\tin_tissue_spots\n' > "$SUM"

for s in $SAMPLES; do
    row=$(awk -F'\t' -v s="$s" '$1 == s' "$SHEET")
    [ -n "$row" ] || { echo "== $s not in $SHEET, skipped"; continue; }
    patient=$(echo "$row" | cut -f2); run=$(echo "$row" | cut -f3)
    r1=$ROOT/$(echo "$row" | cut -f5); r2=$ROOT/$(echo "$row" | cut -f6); tarf=$ROOT/$(echo "$row" | cut -f7)
    D=$OUT/$s
    if [ -f "$D/DONE" ]; then echo "== $s already done, skipped"; continue; fi
    echo "== $(date) $s (patient $patient, $run)"
    for f in "$r1" "$r2" "$tarf"; do [ -s "$f" ] || { echo "missing $f"; continue 2; }; done
    rm -rf "$D/mixcr" "$D/reads"
    mkdir -p "$D/mixcr" "$D/reads"

    tar -xzOf "$tarf" spatial/tissue_positions_list.csv > "$D/tissue_positions.csv" 2>/dev/null \
        || tar -xzOf "$tarf" spatial/tissue_positions.csv > "$D/tissue_positions.csv"
    [ -s "$D/tissue_positions.csv" ] || { echo "no positions file in $tarf"; continue; }

    cd "$D/mixcr" || continue
    $MIXCR analyze shotgun -s hsa --starting-material rna --align "-OsaveOriginalReads=true" \
        --assemble "--write-alignments" "$r2" clones > analyze.log 2>&1
    rc=$?
    if [ $rc -ne 0 ] || [ ! -s clones.clns ]; then
        echo "MiXCR analyze failed (rc=$rc)"; tail -20 analyze.log; cd "$ROOT"; continue
    fi
    $MIXCR exportReadsForClones -s clones.clns ../reads/reads.fastq.gz > export_reads.log 2>&1
    cd "$ROOT" || exit 1
    grep -E "^(Total sequencing reads|Successfully aligned reads|Final clonotype count)" "$D/mixcr/clones.report"

    $PY scripts/visium_tcr_counts.py --reads-dir "$D/reads" --r1 "$r1" --positions "$D/tissue_positions.csv" \
        --clones "$D/mixcr/clones.clonotypes.ALL.txt" --matrix "$D/spot_clone_matrix.tsv" \
        --long "$D/spot_clone_long.tsv" | tee "$D/counts.log"
    [ -s "$D/spot_clone_long.tsv" ] || { echo "counting failed for $s"; continue; }

    if [ "$s" = TEST_pt16_downsample ]; then
        T=data/ref/spatialTCR_pt16_test
        $PY scripts/compare_tcr_counts.py "$T/output_counts.txt" "$T/mixcr_output/clones.clonotypes.ALL.txt" \
            "$D/spot_clone_matrix.tsv" "$D/mixcr/clones.clonotypes.ALL.txt" | tee "$D/compare_to_authors.log"
        if ! grep -q '^MATCH$' "$D/compare_to_authors.log" && [ -z "${FORCE:-}" ]; then
            echo "TEST does not reproduce the authors' counts; stopping before the real samples (FORCE=1 overrides)"
            exit 1
        fi
    fi

    reads=$(awk -F': ' '/^Total sequencing reads/ { print $2; exit }' "$D/mixcr/clones.report")
    aligned=$(awk -F'[()]' '/^Successfully aligned reads/ { print $2; exit }' "$D/mixcr/clones.report")
    nclon=$(awk -F': ' '/^Final clonotype count/ { v = $2 } END { print v }' "$D/mixcr/clones.report")
    ntrb=$(awk 'END { print NR - 1 }' "$D/mixcr/clones.clonotypes.TRB.txt" 2>/dev/null)
    stats=$(awk -F'\t' 'NR > 1 { u += $8; if ($9 == "TRB") { t += $8; trb[$1] = 1; if ($2 == "1") { ti += $8; tin[$1] = 1 } } }
                        END { printf "%d\t%d\t%d\t%d\t%d", u, t, ti, length(trb), length(tin) }' "$D/spot_clone_long.tsv")
    ntis=$(awk -F, '$2 == "1"' "$D/tissue_positions.csv" | wc -l)
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$s" "$patient" "$run" "$reads" "$aligned" "$nclon" "$ntrb" "$stats" "$ntis" >> "$SUM"
    date > "$D/DONE"
done

echo "$(date) done"
column -t -s $'\t' "$SUM"
