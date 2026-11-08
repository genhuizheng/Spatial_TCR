#!/bin/bash
#SBATCH -J xenium_valid
#SBATCH -p gg
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 04:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/xenium_validation_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/xenium_validation_%j.err

# Reproduce McCord et al. 2026 TCR probe validation on all GSE300147 sections
# (metadata/xenium_all_samples.tsv), in two stages:
#   stage 1 (default): joint clustering of all sections (xenium_cluster_all.py) into ~10 clusters;
#            prints lineage scores and top genes per cluster, then stops for hand labelling.
#   stage 2: LABELS=<cluster<TAB>label file> CLUSTERS=<stage-1 folder> sbatch scripts/xenium_validation.slurm
#            probe calls in every section with the shared T cluster (xenium_tcr_calls.py --clusters),
#            then the comparison with the published numbers (xenium_probe_validation.py).
# Outputs: outputs/xenium_validation/<time>_<job>/

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
TOOLS=${TOOLS:-/scratch/10119/ghzheng/tools}
cd "$ROOT" || exit 1
SHEET=${SHEET:-metadata/xenium_all_samples.tsv}
[ -d "$TOOLS/pylib_xenium" ] && export PYTHONPATH=$TOOLS/pylib_xenium${PYTHONPATH:+:$PYTHONPATH}
PYBIN=""
for p in ${PY:-} /scratch/10119/ghzheng/conda_envs/worldmodel_withconfidenceot/bin/python python3; do
    command -v "$p" >/dev/null 2>&1 || [ -x "$p" ] || continue
    if "$p" -c "import numpy, scipy, h5py, pyarrow, scanpy, anndata, leidenalg, igraph" >/dev/null 2>&1; then PYBIN=$p; break; fi
done
[ -n "$PYBIN" ] || { echo "no Python with numpy, scipy, h5py, pyarrow, scanpy, leidenalg, igraph (set PY=...)"; exit 1; }
echo "$(date) $(hostname) python: $PYBIN"
export LOKY_MAX_CPU_COUNT=${SLURM_CPUS_ON_NODE:-8}

RUN=outputs/xenium_validation/$(date +%Y%m%d_%H%M%S)_${SLURM_JOB_ID:-local}
mkdir -p "$RUN"
cp "$SHEET" "$RUN/"
git rev-parse HEAD > "$RUN/git_commit.txt" 2>/dev/null

if [ -z "${LABELS:-}" ]; then
    "$PYBIN" -W ignore scripts/xenium_cluster_all.py --sheet "$SHEET" --out "$RUN/clusters" || exit 1
    echo "stage 1 done. Label the clusters by hand (copy $RUN/clusters/labels_proposed.tsv), then:"
    echo "  LABELS=<labels.tsv> CLUSTERS=$RUN/clusters sbatch scripts/xenium_validation.slurm"
    exit 0
fi

[ -s "$LABELS" ] && [ -s "${CLUSTERS:-}/clusters.tsv" ] || { echo "stage 2 needs LABELS=<file> and CLUSTERS=<stage-1 folder>"; exit 1; }
cp "$LABELS" "$RUN/labels.tsv"
echo "$CLUSTERS" > "$RUN/clusters_from.txt"
for s in $(awk -F'\t' 'NR > 1 { print $1 }' "$SHEET"); do
    prefix=data/raw/$(awk -F'\t' -v s="$s" '$1 == s { print $6 }' "$SHEET")
    echo "== $(date) $s"
    "$PYBIN" -W ignore scripts/xenium_tcr_calls.py --sample "$s" --prefix "$prefix" --probe-group auto \
        --clusters "$CLUSTERS/clusters.tsv" --labels "$LABELS" --out "$RUN/$s/calls" 2>&1 \
        | grep -E "probe groups|in the shared|T-cluster|tcr_own|tcr_other|focal TCR|done|Error|error" \
        || echo "xenium_tcr_calls.py printed nothing for $s"
done
"$PYBIN" scripts/xenium_probe_validation.py --run "$RUN" --sheet "$SHEET" --out "$RUN/validation"
echo "$(date) done -> $RUN"
