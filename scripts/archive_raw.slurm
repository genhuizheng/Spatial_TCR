#!/bin/bash
#SBATCH -J tcr_raw_archive
#SBATCH -p gg
#SBATCH -A MCB26031
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 08:00:00
#SBATCH -o /scratch/10119/ghzheng/spatial_TCR/logs/archive_raw_%j.out
#SBATCH -e /scratch/10119/ghzheng/spatial_TCR/logs/archive_raw_%j.err

# Package each dataset folder under data/raw into TCR_raw_data/<dataset>.tar.zst
# (falls back to pigz/gzip .tar.gz if zstd is absent).
# data/raw is only read; the original files are kept.
# Each archive is checked by listing it back and comparing the member count
# with the source file count; size, count and sha256 go into TCR_raw_data/MANIFEST.tsv.
# Re-running skips datasets already recorded as OK.
# DATASETS="A B"  only process these folders (default: every folder not starting with _)
# REBUILD=1       with DATASETS: rebuild them even if recorded OK; their old MANIFEST rows
#                 are dropped (MANIFEST.tsv is backed up first) and the old archive is only
#                 replaced once the new one passes the count check.

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
SRC=$ROOT/data/raw
DST=${DST:-$ROOT/TCR_raw_data}
THREADS=${THREADS:-$(nproc)}
LEVEL=${LEVEL:-3}

if command -v zstd >/dev/null 2>&1; then
    EXT=tar.zst; COMP="zstd -q -T$THREADS -$LEVEL"; DECOMP="zstd -q -dc -T$THREADS"
elif command -v pigz >/dev/null 2>&1; then
    EXT=tar.gz; COMP="pigz -p $THREADS -$LEVEL"; DECOMP="pigz -dc"
else
    EXT=tar.gz; COMP="gzip -1"; DECOMP="gzip -dc"
fi
echo "$(date) compressor: $COMP  threads: $THREADS  -> $DST"

mkdir -p "$DST"
MAN=$DST/MANIFEST.tsv
[ -f "$MAN" ] || printf 'archive\tsource_dir\tn_files_source\tn_files_archive\tbytes_source\tbytes_archive\tsha256\tcreated_utc\tstatus\n' > "$MAN"

if [ -n "${REBUILD:-}" ]; then
    if [ -z "${DATASETS:-}" ]; then echo "REBUILD needs DATASETS"; exit 1; fi
    cp "$MAN" "$MAN.bak_$(date +%Y%m%d_%H%M%S)"
    for d in $DATASETS; do
        awk -F'\t' -v a="$d.$EXT" -v p="$d.$EXT.part" '$1 != a && $1 != p' "$MAN" > "$MAN.tmp" && mv "$MAN.tmp" "$MAN"
    done
    echo "$(date) rebuilding: $DATASETS (MANIFEST rows dropped, backup kept)"
fi

cd "$SRC" || exit 1
LIST=${DATASETS:-$(ls -d */ | sed 's|/$||' | grep -v '^_')}
for d in $LIST; do
    d=${d%/}
    [ -d "$d" ] || { echo "$(date) no folder $d, skipped"; continue; }
    out=$DST/$d.$EXT
    if grep -q "^$d\.$EXT	.*	OK$" "$MAN"; then
        echo "$(date) skip $d (already archived OK)"
        continue
    fi
    nsrc=$(find "$d" -type f | wc -l)
    bsrc=$(du -sb "$d" | cut -f1)
    echo "$(date) archiving $d: $nsrc files, $bsrc bytes"
    rm -f "$out.part"
    tar -cf - "$d" | $COMP > "$out.part"
    narc=$($DECOMP "$out.part" | tar -tf - | grep -v '/$' | wc -l)
    barc=$(stat -c %s "$out.part")
    if [ "$narc" = "$nsrc" ]; then
        mv "$out.part" "$out"
        status=OK
        target=$out
    else
        status=COUNT_MISMATCH
        target=$out.part
    fi
    sha=$(sha256sum "$target" | cut -d' ' -f1)
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(basename "$target")" "data/raw/$d" "$nsrc" "$narc" \
        "$bsrc" "$barc" "$sha" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$status" >> "$MAN"
    echo "$(date) $d -> $(basename "$target"): $status ($narc/$nsrc files, $barc bytes)"
done

echo "$(date) done"
column -t -s $'\t' "$MAN"
du -sh "$DST"
