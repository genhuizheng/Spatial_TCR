#!/bin/bash
# Read-only checks on small files already in data/raw (fine on the login node):
#   1. GSE296577 (GBM Xenium): README, custom panel members, TCR-like targets, P34_PRE_1 listing
#   2. GSE280314 (CRC Xenium): TCR-like targets in gene_panel.json
#   3. GSE287301 (McCord scRNA/TCR): are per-cell hashtag counts in the aggregated matrix?
#      feature types, barcode suffixes (one per aggregation.csv row), patient_matrix
#   bash scripts/data_checks.sh 2>&1 | tee logs/data_checks_$(date +%Y%m%d).log
# Nothing is written to data/raw; temporary files go to $TMPD and are removed.

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
RAW=$ROOT/data/raw
TMPD=${TMPD:-$ROOT/tmp_data_checks_$$}
TCR_RE='CDR3|TR[AB][VJC][0-9]|TR[AB]C|_TR[AB]|TCR|TRBV|TRAV'
mkdir -p "$TMPD" || exit 1

echo "== 1. GSE296577"
D=$RAW/GSE296577
if [ -d "$D" ]; then
    ls -la "$D"
    echo "-- README (first 80 lines)"
    head -80 "$D/GSE296577_README.txt"
    P=$D/GSE296577_PKK3C7_hBrain_100g_custom_panel.tar.gz
    echo "-- custom panel members"
    tar -tzvf "$P"
    echo "-- TCR-like strings in the custom panel"
    tar -xzOf "$P" 2>/dev/null | grep -a -o -i -E "[A-Za-z0-9_.-]*($TCR_RE)[A-Za-z0-9_.-]*" | sort | uniq -c | sort -rn | head -60
    echo "-- custom panel: first lines of each text member"
    mkdir -p "$TMPD/panel" && tar -xzf "$P" -C "$TMPD/panel"
    find "$TMPD/panel" -type f | while read -r f; do
        echo "## ${f#$TMPD/panel/} ($(wc -l < "$f") lines)"
        head -c 2000 "$f" | head -8; echo
    done
    echo "-- P34_PRE_1 sample tar (first 60 members)"
    for t in "$D"/GSM*_P34_PRE_1.tar.gz; do tar -tzvf "$t" | head -60; done
else
    echo "no $D"
fi

echo
echo "== 2. GSE280314"
J=$RAW/GSE280314/GSE280314_gene_panel.json.gz
if [ -s "$J" ]; then
    echo "-- quoted strings in gene_panel.json: $(zcat "$J" | grep -o '"[^"]*"' | wc -l)"
    echo "-- TCR-like strings"
    zcat "$J" | grep -o -i -E "\"[^\"]*($TCR_RE)[^\"]*\"" | sort | uniq -c | sort -rn | head -60
    echo "-- start of the file"
    zcat "$J" | head -c 1500; echo
else
    echo "no $J"
fi

echo
echo "== 3. GSE287301 hashtags"
D=$RAW/GSE287301
M=$D/GSE287301_filtered_feature_bc_matrix.tar.gz
if [ -s "$M" ]; then
    tar -xzOf "$M" --occurrence=1 features.tsv.gz | zcat > "$TMPD/features.tsv"
    tar -xzOf "$M" --occurrence=1 barcodes.tsv.gz | zcat > "$TMPD/barcodes.tsv"
    echo "-- feature types"
    cut -f3 "$TMPD/features.tsv" | sort | uniq -c
    echo "-- features that are not Gene Expression (first 40)"
    awk -F'\t' '$3 != "Gene Expression"' "$TMPD/features.tsv" | head -40
    echo "-- features named like a hashtag (first 20)"
    grep -i -E 'hash|HTO|TotalSeq|GTCAACTCTTTAGCG|TGATGGCCTATTGGG|TTCCGCCTCTCTTTG|AGTAAGTTCAGCGTA' "$TMPD/features.tsv" | head -20
    echo "-- barcodes: $(wc -l < "$TMPD/barcodes.tsv"); cells per suffix (aggregation.csv order)"
    awk -F'-' '{ print $NF }' "$TMPD/barcodes.tsv" | sort -n | uniq -c
    echo "-- aggregation.csv"
    zcat "$D/GSE287301_aggregation.csv.gz" | cut -d, -f1 | awk 'NR > 1 { print NR - 1 "\t" $0 }'
    echo "-- patient_matrix (hashtag x pool -> patient)"
    zcat "$D/GSE287301_patient_matrix.txt.gz"
    echo "-- VDJ tar members per pool (do any carry per-cell patient or hashtag calls?)"
    for t in "$D"/GSM*.tar.gz; do echo "## $(basename "$t"): $(tar -tzf "$t" | tr '\n' ' ')"; done | head -20
else
    echo "no $M"
fi

rm -rf "$TMPD"
echo
echo "$(date) data checks done"
