#!/bin/bash
#SBATCH -J sctcr_mixcr
#SBATCH -p gg
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 06:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/sctcr_mixcr_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/sctcr_mixcr_%j.err

# Paired TRA/TRB clonotypes for the brain metastasis 10x single-cell VDJ libraries
# (GSE179373 / PRJNA743437, Sudmeier 2022), for linking to the Visium TCR spot calls.
# MiXCR 4.7.0 preset 10x-sc-xcr-vdj (R1 = 16 nt cell barcode + 10 nt UMI, R2 = V(D)J).
# Cell Ranger, the 10x standard, has no ARM build and Vista nodes are ARM (Grace).
# Setup first, on the login node: bash scripts/setup_mixcr.sh
# Reads: data/raw/PRJNA743437/<run>/<run>_{1,2}.fastq.gz (ena_download.py); the two runs of a
# sample are concatenated. SAMPLES="sc_pt15" limits the run; finished samples are skipped.
# Outputs: outputs/sctcr_mixcr/<sample>/ (MiXCR results), headers.txt (export column names)

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
TOOLS=${TOOLS:-/scratch/10119/ghzheng/tools}
MEM=${MEM:-150g}
cd "$ROOT" || exit 1
SHEET=metadata/bm_sctcr_samples.tsv
JAR=$TOOLS/mixcr-4.7.0/mixcr.jar
[ -s "$JAR" ] || { echo "missing $JAR: run bash scripts/setup_mixcr.sh on the login node"; exit 1; }

# MiXCR 4.x needs Java 11+; the system java is 1.8, so use the JDK from setup_mixcr.sh
JAVA=${JAVA:-$TOOLS/jdk-17.0.21+9/bin/java}
[ -x "$JAVA" ] || { echo "missing $JAVA: run bash scripts/setup_mixcr.sh on the login node"; exit 1; }
$JAVA -Xmx256m -version >/dev/null 2>&1 || { echo "$JAVA does not run"; exit 1; }
if [ -z "${MI_LICENSE:-}" ] && [ -z "${MI_LICENSE_FILE:-}" ] && [ -s "$HOME/mi.license" ]; then
    export MI_LICENSE_FILE=$HOME/mi.license
fi
[ -n "${MI_LICENSE:-}${MI_LICENSE_FILE:-}" ] || { echo "no MiXCR license: save the key to \$HOME/mi.license"; exit 1; }
export MI_STAT_DISABLE=1
MIXCR="$JAVA -Xmx$MEM -jar $JAR"
echo "$(date) $($JAVA -version 2>&1 | head -1)  MiXCR: $($MIXCR -v 2>&1 | head -1)"
$MIXCR -v >/dev/null 2>&1 || { echo "MiXCR does not start:"; $MIXCR -v 2>&1 | tail -5; exit 1; }

SAMPLES=${SAMPLES:-$(awk -F'\t' 'NR > 1 { print $1 }' "$SHEET")}
OUT=$ROOT/outputs/sctcr_mixcr
mkdir -p "$OUT"

for s in $SAMPLES; do
    row=$(awk -F'\t' -v s="$s" '$1 == s' "$SHEET")
    [ -n "$row" ] || { echo "== $s not in $SHEET, skipped"; continue; }
    D=$OUT/$s
    if [ -f "$D/DONE" ]; then echo "== $s already done, skipped"; continue; fi
    echo "== $(date) $s ($(echo "$row" | cut -f3,4))"
    rm -rf "$D"; mkdir -p "$D"
    r1=""; r2=""
    for run in $(echo "$row" | cut -f5 | tr ',' ' '); do
        for k in 1 2; do
            f=data/raw/PRJNA743437/$run/${run}_$k.fastq.gz
            [ -s "$f" ] || { echo "missing $f"; continue 3; }
        done
        r1="$r1 data/raw/PRJNA743437/$run/${run}_1.fastq.gz"
        r2="$r2 data/raw/PRJNA743437/$run/${run}_2.fastq.gz"
    done
    # 10x layout check: read 1 must be 26 nt (barcode + UMI) and read 2 longer
    l1=$(zcat $r1 | head -2 | tail -1 | tr -d '\n' | wc -c)
    l2=$(zcat $r2 | head -2 | tail -1 | tr -d '\n' | wc -c)
    echo "read lengths: R1 $l1, R2 $l2"
    if [ "$l1" -lt 26 ] || [ "$l2" -le "$l1" ]; then echo "unexpected read layout, $s skipped"; continue; fi
    cat $r1 > "$D/R1.fastq.gz"
    cat $r2 > "$D/R2.fastq.gz"

    cd "$D" || continue
    $MIXCR analyze 10x-sc-xcr-vdj --species hsa R1.fastq.gz R2.fastq.gz result > analyze.log 2>&1
    rc=$?
    cd "$ROOT" || exit 1
    if [ $rc -ne 0 ]; then
        echo "MiXCR analyze failed (rc=$rc)"; tail -20 "$D/analyze.log"
        if grep -qi "licen" "$D/analyze.log"; then echo "license problem: stopping"; exit 1; fi
        continue
    fi
    rm -f "$D/R1.fastq.gz" "$D/R2.fastq.gz"
    ls -la "$D"
    for t in "$D"/*.tsv; do
        echo "## $(basename "$t"): $(($(wc -l < "$t") - 1)) rows"
        head -1 "$t" | tr '\t' '\n' | paste -sd' '
    done | tee "$D/headers.txt"
    grep -hE "cell|Cell|clonotype|Total sequencing reads|Successfully aligned" "$D"/*.report.txt 2>/dev/null | head -30
    date > "$D/DONE"
done

echo "$(date) done"
