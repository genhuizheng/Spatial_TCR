#!/bin/bash
#SBATCH -J xenium_shells
#SBATCH -p gh
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 02:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/xenium_shells_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/xenium_shells_%j.err

# TCR-centred shells (shell 0 + fine physical rings + Delaunay hops) for the Xenium pilot
# samples in metadata/xenium_pilot_samples.tsv (McCord Patient 19, runs 1 and 2), then the
# three shell-0 views are checked for each sample and scheme.
# Outputs go to a new run-stamped folder: outputs/xenium_shells/<time>_<job>/<sample>/
# Options (environment): SAMPLES="p19_run1"  WIDTH=auto|<um>  MAX_RADIUS=250  MAX_HOPS=25
#                        MAX_EDGE=<um> (prune Delaunay edges; default none)  PY=<python>

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
cd "$ROOT" || exit 1
SHEET=metadata/xenium_pilot_samples.tsv

PYBIN=""
for p in ${PY:-} /scratch/10119/ghzheng/conda_envs/worldmodel_withconfidenceot/bin/python python3; do
    command -v "$p" >/dev/null 2>&1 || [ -x "$p" ] || continue
    if "$p" -c "import numpy, scipy, h5py, pyarrow" >/dev/null 2>&1; then PYBIN=$p; break; fi
done
[ -n "$PYBIN" ] || { echo "no Python with numpy, scipy, h5py and pyarrow (set PY=...)"; exit 1; }
echo "$(date) $(hostname) python: $PYBIN ($("$PYBIN" --version 2>&1))"

RUN=outputs/xenium_shells/$(date +%Y%m%d_%H%M%S)_${SLURM_JOB_ID:-local}
mkdir -p "$RUN"
cp "$SHEET" "$RUN/"
git rev-parse HEAD > "$RUN/git_commit.txt" 2>/dev/null
SAMPLES=${SAMPLES:-$(awk -F'\t' 'NR > 1 { print $1 }' "$SHEET")}
EXTRA=""
[ -n "${MAX_EDGE:-}" ] && EXTRA="--max-edge $MAX_EDGE"

for s in $SAMPLES; do
    row=$(awk -F'\t' -v s="$s" '$1 == s' "$SHEET")
    [ -n "$row" ] || { echo "== $s not in $SHEET, skipped"; continue; }
    group=$(echo "$row" | cut -f5)
    prefix=data/raw/$(echo "$row" | cut -f6)
    echo "== $(date) $s ($(echo "$row" | cut -f2-4 | tr '\t' ' '), probe group $group)"
    for f in "${prefix}_cells.parquet.gz" "${prefix}_cell_feature_matrix.h5"; do
        [ -s "$f" ] || { echo "missing $f"; continue 2; }
    done
    "$PYBIN" scripts/xenium_shells.py --sample "$s" --prefix "$prefix" --probe-group "$group" \
        --out "$RUN/$s" --width "${WIDTH:-auto}" --max-radius "${MAX_RADIUS:-250}" --max-hops "${MAX_HOPS:-25}" $EXTRA \
        || { echo "xenium_shells.py failed for $s"; continue; }
    for sc in physical graph; do
        "$PYBIN" scripts/xenium_shell_views.py "$RUN/$s" --scheme $sc
    done
    "$PYBIN" scripts/xenium_shell_views.py "$RUN/$s" --scheme physical --merge 25,75,150 | tail -3
    echo "-- top own-patient probes"
    (head -1 "$RUN/$s/tcr_probe_qc.tsv"; awk -F'\t' '$3 == "tcr_own"' "$RUN/$s/tcr_probe_qc.tsv" | sort -t$'\t' -k6,6nr | head -15) | column -t -s $'\t'
    ls -la "$RUN/$s"
done

echo "$(date) done -> $RUN"
du -sh "$RUN"
