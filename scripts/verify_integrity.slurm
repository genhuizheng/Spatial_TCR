#!/bin/bash
#SBATCH -J tcr_integrity
#SBATCH -p gg
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 02:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/integrity_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/integrity_%j.err

# Full content check of every downloaded file that has no published checksum
# (GEO publishes none). Read-only.
#   *.gz / *.tgz   gzip -t: decompresses the whole stream and checks the CRC
#   *.h5 / *.h5ad  HDF5 signature in the first 8 bytes
#   *.tar          tar -tf lists the whole archive
#   *.zip          unzip -tq tests every member CRC
#   anything else  must not start with an HTML/XML error page
# Output: logs/integrity_<job>.out ends with a BAD list (empty means all good).
# Dryad and OSF files were already checked against published SHA-256 digests.

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
JOBS=${JOBS:-$(nproc)}
cd "$ROOT/data/raw" || exit 1
DIRS=${DIRS:-$(ls -d GSE* SCP1348 2>/dev/null)}
REPORT=$ROOT/logs/integrity_${SLURM_JOB_ID:-manual}.tsv
echo "$(date) checking: $DIRS with $JOBS parallel workers"

check_one() {
    f=$1
    case "$f" in
        *.gz|*.tgz)        gzip -t "$f" 2>/dev/null && r=OK || r=BAD_GZIP ;;
        *.h5|*.h5ad|*.hdf5) [ "$(head -c 8 "$f" | od -An -tx1 | tr -d ' \n')" = "894844460d0a1a0a" ] && r=OK || r=BAD_HDF5_SIGNATURE ;;
        *.tar)             tar -tf "$f" > /dev/null 2>&1 && r=OK || r=BAD_TAR ;;
        *.zip)             unzip -tq "$f" > /dev/null 2>&1 && r=OK || r=BAD_ZIP ;;
        *)                 head -c 200 "$f" | grep -q -a -E '^[[:space:]]*(<\?xml|<!DOCTYPE|<html)' && r=BAD_ERROR_PAGE || r=OK ;;
    esac
    [ -s "$f" ] || r=EMPTY
    printf '%s\t%s\t%s\n' "$r" "$(stat -c %s "$f")" "$f"
}
export -f check_one

find $DIRS -type f ! -name 'cfg*.txt' ! -name 'provenance*.tsv' -print0 \
    | xargs -0 -P "$JOBS" -I{} bash -c 'check_one "$1"' _ {} > "$REPORT"

echo "$(date) done: $(wc -l < "$REPORT") files checked"
cut -f1 "$REPORT" | sort | uniq -c
echo "== BAD or EMPTY:"
grep -v '^OK' "$REPORT" | sort -k3
