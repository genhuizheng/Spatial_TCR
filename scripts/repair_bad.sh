#!/bin/bash
# Re-download the GEO files that verify_integrity.slurm reported as BAD.
# Usage (login node, under nohup):  bash scripts/repair_bad.sh logs/integrity_<job>.tsv
#
# 1. Records the first bytes and the gzip error of each bad file.
# 2. Moves each bad file (never deletes it) to data/raw/_quarantine_<time>/<series>/.
# 3. Re-downloads exactly those files with geo_download.py --verify-gzip.
# 4. Tests the new copy and compares it with the quarantined one:
#      FIXED            new copy passes the check
#      BAD_AT_SOURCE    new copy fails and is byte-identical to the old one, so the file
#                       on GEO itself is broken (two independent downloads agree)
#      STILL_BAD        new copy fails and differs from the old one: run this again
#      NOT_DOWNLOADED   no new copy; the quarantined copy is still available
# EMPTY rows are ignored (GSM7658221 is a genuine 0-byte upload).
# The quarantine directory is left for the user to remove after reading the summary.

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
TSV=$1
cd "$ROOT" || exit 1
if [ -z "$TSV" ] || [ ! -s "$TSV" ]; then echo "usage: bash scripts/repair_bad.sh logs/integrity_<job>.tsv"; exit 1; fi

Q=data/raw/_quarantine_$(date +%Y%m%d_%H%M%S)
mkdir -p "$Q"
LIST=$Q/bad_list.tsv
grep '^BAD' "$TSV" | sort -k3 > "$LIST"
echo "$(date) $(wc -l < "$LIST") bad files; quarantine: $Q"

check() {
    case "$1" in
        *.gz|*.tgz)         gzip -t "$1" 2>/dev/null ;;
        *.h5|*.h5ad|*.hdf5) [ "$(head -c 8 "$1" | od -An -tx1 | tr -d ' \n')" = "894844460d0a1a0a" ] ;;
        *.tar)              tar -tf "$1" > /dev/null 2>&1 ;;
        *.zip)              unzip -tq "$1" > /dev/null 2>&1 ;;
        *)                  ! head -c 200 "$1" | grep -q -a -E '^[[:space:]]*(<\?xml|<!DOCTYPE|<html)' ;;
    esac
}

echo "== diagnosis of the old copies"
while IFS=$'\t' read -r st sz rel; do
    f=data/raw/$rel
    if [ ! -f "$f" ]; then echo "missing: $f"; continue; fi
    head_txt=$(head -c 24 "$f" | od -An -c | tr -s ' \n' ' ' | cut -c1-80)
    gz_msg=""
    case "$f" in *.gz|*.tgz) gz_msg=$(gzip -t "$f" 2>&1 | tail -1 | sed "s|$f||" | cut -c1-80) ;; esac
    echo "$rel"
    echo "    head: $head_txt"
    [ -n "$gz_msg" ] && echo "    gzip: $gz_msg"
    mkdir -p "$Q/$(dirname "$rel")"
    mv "$f" "$Q/$rel"
done < "$LIST"

for ds in $(cut -f3 "$LIST" | cut -d/ -f1 | sort -u); do
    case "$ds" in GSE*) ;; *) echo "== $ds is not a GEO series; re-download it by hand"; continue ;; esac
    re=$(awk -F'\t' -v d="$ds/" 'index($3, d) == 1 { n = split($3, p, "/"); print p[n] }' "$LIST" \
         | sed 's/[.]/[.]/g' | paste -sd'|')
    echo "== re-download $ds: ^($re)\$"
    python3 scripts/geo_download.py --out data/raw --cache data/raw/geo_meta --workers 2 \
        --verify-gzip --include "^($re)\$" "$ds"
done

echo "== summary"
while IFS=$'\t' read -r st sz rel; do
    f=data/raw/$rel
    if [ ! -s "$f" ]; then r=NOT_DOWNLOADED
    elif check "$f"; then r=FIXED
    elif cmp -s "$f" "$Q/$rel"; then r=BAD_AT_SOURCE
    else r=STILL_BAD
    fi
    printf '%s\t%s\t%s\n' "$r" "$(stat -c %s "$f" 2>/dev/null || echo 0)" "$rel"
done < "$LIST" | tee "$Q/summary.tsv"
echo "$(date) done. Counts:"
cut -f1 "$Q/summary.tsv" | sort | uniq -c
echo "Old copies are in $Q (remove after checking the summary)."
