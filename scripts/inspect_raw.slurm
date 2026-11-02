#!/bin/bash
#SBATCH -J tcr_raw_inspect
#SBATCH -p gg
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 02:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/inspect_raw_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/inspect_raw_%j.err

# Read-only inspection of data/raw. Writes:
#   metadata/RAW_DATA_FORMATS.md      what every file kind contains
#   metadata/raw_file_inventory.tsv   one row per file
# Picks the first Python that has both pyarrow and h5py (override with PY=...).

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
cd "$ROOT" || exit 1

CANDIDATES="${PY:-} /scratch/10119/ghzheng/conda_envs/worldmodel_withconfidenceot/bin/python python3"
PYBIN=""
for p in $CANDIDATES; do
    command -v "$p" >/dev/null 2>&1 || [ -x "$p" ] || continue
    if "$p" -c "import pyarrow, h5py" >/dev/null 2>&1; then PYBIN=$p; break; fi
    if [ -z "${FALLBACK:-}" ] && "$p" -c "import h5py" >/dev/null 2>&1; then FALLBACK=$p; fi
done
if [ -z "$PYBIN" ]; then
    PYBIN=${FALLBACK:-python3}
    echo "WARNING: no Python with both pyarrow and h5py; using $PYBIN (the report lists what is missing)"
fi
echo "python: $PYBIN ($("$PYBIN" --version 2>&1))"

export TMPDIR=$ROOT/tmp_inspect_$SLURM_JOB_ID
mkdir -p "$TMPDIR" metadata
"$PYBIN" scripts/inspect_raw.py --root data/raw \
    --out metadata/RAW_DATA_FORMATS.md --inventory metadata/raw_file_inventory.tsv
rc=$?
rm -rf "$TMPDIR"
echo "inspect_raw exit code: $rc"
ls -la metadata/RAW_DATA_FORMATS.md metadata/raw_file_inventory.tsv
