#!/bin/bash
# Copy the raw-data archives built by archive_raw.slurm to Corral and verify every copy against
# the sha256 recorded in MANIFEST.tsv. Run on a login node (Corral is not writable from compute
# nodes, which is why archive_raw.slurm fell back to $ROOT/TCR_raw_data_corral):
#   nohup bash scripts/copy_archive_to_corral.sh > logs/corral_copy_$(date +%Y%m%d_%H%M).log 2>&1 &
# Resumable (rsync --partial); re-running re-checks everything. The scratch copy is never deleted.
# SRC=<scratch archive folder>  DST=<Corral folder>  override the defaults.
# RSYNC_OPTS=--checksum  re-copies files whose content differs (use if a verify reports MISMATCH).

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
SRC=${SRC:-$ROOT/TCR_raw_data_corral}
DST=${DST:-/corral/utexas/MCB26031/genhui/TCR_raw_data}

echo "$(date) $(hostname) $SRC -> $DST"
[ -s "$SRC/MANIFEST.tsv" ] || { echo "no $SRC/MANIFEST.tsv"; exit 1; }
nok=$(awk -F'\t' 'NR > 1 && $9 == "OK"' "$SRC/MANIFEST.tsv" | wc -l)
nbad=$(awk -F'\t' 'NR > 1 && $9 != "OK"' "$SRC/MANIFEST.tsv" | wc -l)
echo "MANIFEST: $nok archives OK, $nbad not OK; source size $(du -sh "$SRC" | cut -f1)"

mkdir -p "$DST" || { echo "cannot create $DST"; exit 1; }
touch "$DST/.write_test" 2>/dev/null || { echo "$DST is not writable from $(hostname)"; exit 1; }
rm -f "$DST/.write_test"

nice rsync -a --partial ${RSYNC_OPTS:-} --exclude '*.part' "$SRC/" "$DST/"
rc=$?
echo "$(date) rsync exit code $rc"
[ $rc -eq 0 ] || { echo "rsync failed; re-run to resume"; exit 1; }

cd "$DST" || exit 1
good=0; bad=0
while IFS=$'\t' read -r arc _ _ _ _ bytes sha _ status; do
    [ "$status" = OK ] || continue
    got=$(nice sha256sum "$arc" 2>/dev/null | cut -d' ' -f1)
    size=$(stat -c %s "$arc" 2>/dev/null)
    if [ "$got" = "$sha" ] && [ "$size" = "$bytes" ]; then
        good=$((good + 1)); echo "verified  $arc"
    else
        bad=$((bad + 1)); echo "MISMATCH  $arc (size $size, expected $bytes)"
    fi
done < <(tail -n +2 MANIFEST.tsv)

echo "$(date) $good of $nok archives verified on Corral, $bad mismatched"
[ $bad -eq 0 ] && [ $good -eq "$nok" ] && echo "ALL VERIFIED: $DST ($(du -sh "$DST" | cut -f1)); scratch copy $SRC kept"
