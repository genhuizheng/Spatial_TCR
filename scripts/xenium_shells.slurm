#!/bin/bash
#SBATCH -J xenium_shells
#SBATCH -p gh
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 02:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/xenium_shells_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/xenium_shells_%j.err

# Xenium pilot (metadata/xenium_pilot_samples.tsv, McCord Patient 19 runs 1 and 2), per sample:
#   1. xenium_tcr_calls.py: gene-only Leiden clusters, McCord probe rule, mismatched-probe tiers
#   2. xenium_shells.py --calls: shell 0 + fine physical rings + Delaunay hops for tier_mccord cells
#   3. xenium_shell_views.py: the three shell-0 views, all focal cells and the strict tier
# Outputs go to a new run-stamped folder: outputs/xenium_shells/<time>_<job>/<sample>/{calls,shells}
# Step 1 needs scanpy + leidenalg + igraph. If the env lacks them, install once on the login node:
#   python3 -m pip install --target /scratch/10119/ghzheng/tools/pylib_xenium scanpy leidenalg igraph
# (that folder is added to PYTHONPATH here; nothing is installed into the conda env).
# Options (environment): SAMPLES="p19_run1"  WIDTH=auto|<um>  MAX_RADIUS=250  MAX_HOPS=25
#   MAX_EDGE=<um> (prune Delaunay edges)  RESOLUTION=0.8  LABELS_<sample>=<cluster label TSV>
#   NO_CALLS=1 (old --min-cells rule, no clustering)  PY=<python>

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
TOOLS=${TOOLS:-/scratch/10119/ghzheng/tools}
cd "$ROOT" || exit 1
SHEET=metadata/xenium_pilot_samples.tsv
[ -d "$TOOLS/pylib_xenium" ] && export PYTHONPATH=$TOOLS/pylib_xenium${PYTHONPATH:+:$PYTHONPATH}

PYBIN=""
for p in ${PY:-} /scratch/10119/ghzheng/conda_envs/worldmodel_withconfidenceot/bin/python python3; do
    command -v "$p" >/dev/null 2>&1 || [ -x "$p" ] || continue
    if "$p" -c "import numpy, scipy, h5py, pyarrow" >/dev/null 2>&1; then PYBIN=$p; break; fi
done
[ -n "$PYBIN" ] || { echo "no Python with numpy, scipy, h5py and pyarrow (set PY=...)"; exit 1; }
echo "$(date) $(hostname) python: $PYBIN ($("$PYBIN" --version 2>&1))"
if [ -z "${NO_CALLS:-}" ]; then
    "$PYBIN" -c "import scanpy, anndata, leidenalg, igraph" 2>/dev/null || {
        echo "$PYBIN lacks scanpy/leidenalg/igraph; on the login node run:"
        echo "  $PYBIN -m pip install --target $TOOLS/pylib_xenium scanpy leidenalg igraph"
        exit 1; }
    echo "scanpy $("$PYBIN" -c 'import importlib.metadata as m; print(m.version("scanpy"), "leidenalg", m.version("leidenalg"))')"
fi
export LOKY_MAX_CPU_COUNT=${SLURM_CPUS_ON_NODE:-8}

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
    CALLS=""
    if [ -z "${NO_CALLS:-}" ]; then
        lab=$(eval echo "\${LABELS_$s:-}")
        "$PYBIN" -W ignore scripts/xenium_tcr_calls.py --sample "$s" --prefix "$prefix" --probe-group "$group" \
            --out "$RUN/$s/calls" --resolution "${RESOLUTION:-0.8}" ${lab:+--labels "$lab"} \
            || { echo "xenium_tcr_calls.py failed for $s"; continue; }
        echo "-- own probes"
        awk -F'\t' 'NR == 1 || $2 == "tcr_own"' "$RUN/$s/calls/probe_calls.tsv" | cut -f1,6,7,8,11,12,15,17,19 | column -t -s $'\t'
        echo "-- other-patient probes passing the McCord rule (should be few)"
        awk -F'\t' 'NR > 1 && $2 == "tcr_other" && $15 == "yes"' "$RUN/$s/calls/probe_calls.tsv" | cut -f1,6,7,8,11,12,15 | column -t -s $'\t'
        CALLS="--calls $RUN/$s/calls"
    fi
    "$PYBIN" scripts/xenium_shells.py --sample "$s" --prefix "$prefix" --probe-group "$group" \
        --out "$RUN/$s/shells" --width "${WIDTH:-auto}" --max-radius "${MAX_RADIUS:-250}" --max-hops "${MAX_HOPS:-25}" $EXTRA $CALLS \
        || { echo "xenium_shells.py failed for $s"; continue; }
    for sc in physical graph; do
        "$PYBIN" scripts/xenium_shell_views.py "$RUN/$s/shells" --scheme $sc | tail -1
        [ -n "$CALLS" ] && "$PYBIN" scripts/xenium_shell_views.py "$RUN/$s/shells" --scheme $sc --strict | tail -1
    done
    "$PYBIN" scripts/xenium_shell_views.py "$RUN/$s/shells" --scheme physical --merge 25,75,150 | tail -2
    du -sh "$RUN/$s"
done

echo "$(date) done -> $RUN"
du -sh "$RUN"
