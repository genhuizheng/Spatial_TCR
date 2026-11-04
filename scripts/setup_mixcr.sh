#!/bin/bash
# Login-node setup for the Visium TCR pipeline (downloads only, nothing is run).
#   1. MiXCR 3.0.13, the version used by Hudson and Sudmeier 2022, checked by SHA-256.
#      License: free for research by non-profit institutions (LICENSE inside the zip).
#   2. The authors' downsampled patient 16 test set and expected output, pinned to
#      github.com/whhudson/spatialTCR commit 6347f12, used by visium_tcr.slurm to check
#      that this installation reproduces their published counts exactly.
# Re-running skips anything already present and verified.

ROOT=${ROOT:-/scratch/10119/ghzheng/spatial_TCR}
TOOLS=${TOOLS:-/scratch/10119/ghzheng/tools}
ZIP_URL=https://github.com/milaboratory/mixcr/releases/download/v3.0.13/mixcr-3.0.13.zip
ZIP_SHA=9dccf7e8af84d48d7a071aab2e049db23bd5c6b5bb690f0600ebec207f71d107
REPO=https://raw.githubusercontent.com/whhudson/spatialTCR/6347f125210ad9a616dfc777de7d1e7581942d50

mkdir -p "$TOOLS"
cd "$TOOLS" || exit 1
if [ -s mixcr-3.0.13/mixcr.jar ]; then
    echo "MiXCR already unpacked: $TOOLS/mixcr-3.0.13"
else
    curl -sS -L --fail --retry 5 -o mixcr-3.0.13.zip "$ZIP_URL"
    got=$(sha256sum mixcr-3.0.13.zip | cut -d' ' -f1)
    if [ "$got" != "$ZIP_SHA" ]; then
        echo "SHA-256 mismatch for mixcr-3.0.13.zip: $got"; rm -f mixcr-3.0.13.zip; exit 1
    fi
    unzip -q mixcr-3.0.13.zip && rm -f mixcr-3.0.13.zip
    echo "MiXCR 3.0.13 unpacked: $TOOLS/mixcr-3.0.13 (sha256 OK)"
fi

# MiXCR 4.7.0 for the matched 10x single-cell VDJ libraries (preset 10x-sc-xcr-vdj; 3.0.13
# has no 10x mode, and Cell Ranger has no ARM build for Vista). Same license key.
if [ -s mixcr-4.7.0/mixcr.jar ]; then
    echo "MiXCR 4.7.0 already unpacked: $TOOLS/mixcr-4.7.0"
else
    curl -sS -L --fail --retry 5 -o mixcr-4.7.0.zip \
        https://github.com/milaboratory/mixcr/releases/download/v4.7.0/mixcr-4.7.0.zip
    got=$(sha256sum mixcr-4.7.0.zip | cut -d' ' -f1)
    if [ "$got" != 4fde83750f1d1308ba6b7431bcafe98297b361da7e17efc4d072ed935045cac7 ]; then
        echo "SHA-256 mismatch for mixcr-4.7.0.zip: $got"; rm -f mixcr-4.7.0.zip; exit 1
    fi
    unzip -q -d mixcr-4.7.0 mixcr-4.7.0.zip && rm -f mixcr-4.7.0.zip
    echo "MiXCR 4.7.0 unpacked: $TOOLS/mixcr-4.7.0 (sha256 OK)"
fi

# MiXCR 4.x needs Java 11+ (class files are version 55); the Vista system java is 1.8.
# Eclipse Temurin 17 for ARM (Vista is aarch64), checksum from api.adoptium.net.
JDK=jdk-17.0.21+9
if [ -x "$JDK/bin/java" ]; then
    echo "JDK already unpacked: $TOOLS/$JDK"
elif [ "$(uname -m)" != aarch64 ]; then
    echo "not aarch64 ($(uname -m)): fetch the matching Temurin 17 build instead"
else
    curl -sS -L --fail --retry 5 -o jdk17.tar.gz \
        "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.21%2B9/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.21_9.tar.gz"
    got=$(sha256sum jdk17.tar.gz | cut -d' ' -f1)
    if [ "$got" != 3e4eca7ead088f080af1476007decf010a240a1eb4e1e78c54fa32fbcc347084 ]; then
        echo "SHA-256 mismatch for the JDK: $got"; rm -f jdk17.tar.gz; exit 1
    fi
    tar -xzf jdk17.tar.gz && rm -f jdk17.tar.gz
    echo "JDK unpacked: $TOOLS/$JDK (sha256 OK): $("$JDK/bin/java" -Xmx64m -version 2>&1 | head -1)"
fi

T=$ROOT/data/ref/spatialTCR_pt16_test
mkdir -p "$T/mixcr_output"
cd "$T" || exit 1
for f in downsampled_reads/pt16_downsample_L001_R1_001.fastq.gz downsampled_reads/pt16_downsample_L001_R2_001.fastq.gz \
         code_samples/output_counts.txt code_samples/combine_counts.py \
         mixcr_output/clones.clonotypes.ALL.txt mixcr_output/clones.report \
         spaceranger_output/spatial/tissue_positions_list.csv README.md; do
    out=$(basename "$f")
    case "$f" in mixcr_output/*) out=mixcr_output/$out ;; esac
    [ -s "$out" ] && continue
    curl -sS -L --fail --retry 5 -o "$out" "$REPO/$f" || { echo "FAILED: $f"; rm -f "$out"; }
done
for f in pt16_downsample_L001_R1_001.fastq.gz pt16_downsample_L001_R2_001.fastq.gz; do
    gzip -t "$f" && echo "OK  $f" || echo "BAD $f"
done
ls -la "$T" "$T/mixcr_output"
