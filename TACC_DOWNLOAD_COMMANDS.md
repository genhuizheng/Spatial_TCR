# TACC download plan and commands (spatial TCR project)

Written 2026-11-01. Everything below runs on the **Vista login node** (downloads are
pure network I/O, which is the one kind of work allowed there). Nothing is submitted
to a queue. All paths are under `/scratch/10119/ghzheng/spatial_TCR`.

Scripts live locally in `D:\Xia_lab\spatial_TCR\scripts\` and are copied over with scp.
Every script is standard-library Python 3 plus system `curl`, resumes partial files,
verifies sizes (and digests where the source publishes them) and appends to a
`provenance.tsv` next to the data.

## What gets downloaded, and why

| Target | Source | Size (first pass) | Notes |
|---|---|---|---|
| GSE300147 (Xenium HNSCC + patient-specific CDR3 probes, McCord 2026) | GEO | ~56 GB per-sample files | 18 samples, incl. morphology `.ome.tif.gz` and 14 newer `.tif.gz` images. GSE*_RAW.tar is excluded because it repeats the per-sample files. |
| GSE287301 (matched scRNA + scTCR, 28 HNSCC patients) | GEO | unknown until dry-run | Needed to link probe CDR3s to full clonotypes and patients. |
| GSE285951 (matched PBMC TCR) | GEO | unknown until dry-run | Lower priority; small. |
| GSE238071 (SPTCR-seq spot-level TCR tables, 9 GBM) | GEO | 70 MB | GSM7658221 (UKF260) is a 0-byte author upload. |
| Dryad 10.5061/dryad.h70rxwdmj (Visium + IMC + MALDI + methylation + scRNA, Freiburg GBM) | Dryad API | 10.5 GB (7 files, sha-256 published) | `10XVisium_2.zip` (7.9 GB) is the spatial transcriptome that SPTCR-seq maps onto. |
| OSF 8qbdz (Integrated ST+MALDI RDS objects, 6 GBM) | OSF API, view-only token | 3.0 GB | From the Ravi 2022 Cancer Cell paper; SPTCR paper points here. |
| OSF 65y3t (SPTCR-seq processed objects, NCEM, figure sources) | OSF API, view-only token | 1.1 GB | `Raw_SPTCR_seq.rds` is 120 bytes on OSF itself. |
| GSE179572 (Visium brain metastases, 6 patients, Sudmeier 2022) | GEO | ~3 GB | Spatial images tar 2.7 GB. SRA TCR fastqs (6 runs) not in pass 1. |
| SCP1348 (Slide-TCR-seq, Liu 2022 Immunity) | Broad Single Cell Portal, needs sign-in | ~60 GB after dropping 26 `*.pickle` (377 GB) | Bulk-download cfg carries signed URLs that expire after ~1 day. |
| In situ sequencing TCR (Magoulopoulou 2026, EBioMedicine) | TissUUmaps servers at SciLifeLab | TBD | No repository; see section 6. |

Skipped on purpose: GSE164177 (non-spatial benchmark), circVDJ-seq / SpaCir-VDJ (preprints, no data yet),
SCP1348 Puck_object pickles.

## 0. One-time setup

On TACC:

```bash
mkdir -p /scratch/10119/ghzheng/spatial_TCR/scripts /scratch/10119/ghzheng/spatial_TCR/metadata /scratch/10119/ghzheng/spatial_TCR/logs /scratch/10119/ghzheng/spatial_TCR/data/raw
```

From the local Windows terminal (one command, five files):

```bash
scp D:\Xia_lab\spatial_TCR\scripts\geo_audit.py D:\Xia_lab\spatial_TCR\scripts\geo_download.py D:\Xia_lab\spatial_TCR\scripts\dryad_download.py D:\Xia_lab\spatial_TCR\scripts\osf_download.py D:\Xia_lab\spatial_TCR\scripts\scp_filter_cfg.py ghzheng@vista.tacc.utexas.edu:/scratch/10119/ghzheng/spatial_TCR/scripts/
```

Check python3 and curl on the login node:

```bash
python3 --version; curl --version | head -1
```

## 1. GEO: dry-run first (lists every file with size, downloads nothing)

```bash
cd /scratch/10119/ghzheng/spatial_TCR && python3 scripts/geo_download.py --out data/raw --cache data/raw/geo_meta --dry-run --exclude "_RAW.tar$" GSE300147 GSE287301 GSE285951 GSE238071 GSE179572 2>&1 | tee logs/geo_dryrun_$(date +%Y%m%d).log
```

Paste the `total` lines back. Then the real run, detached:

```bash
cd /scratch/10119/ghzheng/spatial_TCR && nohup python3 scripts/geo_download.py --out data/raw --cache data/raw/geo_meta --workers 3 --exclude "_RAW.tar$" GSE300147 GSE287301 GSE285951 GSE238071 GSE179572 > logs/geo_download_$(date +%Y%m%d).log 2>&1 &
```

Progress check:

```bash
tail -5 /scratch/10119/ghzheng/spatial_TCR/logs/geo_download_*.log; grep -c downloaded /scratch/10119/ghzheng/spatial_TCR/data/raw/provenance.tsv; grep FAILED /scratch/10119/ghzheng/spatial_TCR/data/raw/provenance.tsv
```

Re-running the same command later only fetches what is missing or incomplete.

## 2. Dryad (SPTCR-seq Visium and the rest of the Freiburg multi-omics) -- DONE 2026-11-01

Dryad file downloads now require a bearer token (an unauthenticated request gets
401 `must have current bearer token`). The local copy in
`F:\Tcellworldmodel\SPTCR-seq\Data` matched all 7 published SHA-256 digests, so it
was uploaded with scp instead, and re-verified on TACC (all OK, 2026-11-01):

```bash
cd /scratch/10119/ghzheng/spatial_TCR/data/raw/dryad_h70rxwdmj && sha256sum -c ../../../metadata/dryad_h70rxwdmj.sha256
```

To download from Dryad itself later, create an API account at https://datadryad.org/account,
then (the secret is read without echo and never appears on a command line):

```bash
read -r -p "Dryad client id: " DRYAD_CLIENT_ID; read -r -s -p "Dryad secret: " DRYAD_CLIENT_SECRET; echo; export DRYAD_CLIENT_ID DRYAD_CLIENT_SECRET; cd /scratch/10119/ghzheng/spatial_TCR && nohup python3 scripts/dryad_download.py --out data/raw/dryad_h70rxwdmj 10.5061/dryad.h70rxwdmj > logs/dryad_$(date +%Y%m%d).log 2>&1 &
```

## 3. OSF (two SPTCR-related projects, view-only tokens from the paper)

```bash
cd /scratch/10119/ghzheng/spatial_TCR && nohup sh -c 'python3 scripts/osf_download.py 8qbdz --view-only 5287d7f6263e4ba680ca8c396aeefeee --out data/raw/osf_8qbdz; python3 scripts/osf_download.py 65y3t --view-only 6571f0c374ce4bf294b9cbd10ade62cf --out data/raw/osf_65y3t' > logs/osf_$(date +%Y%m%d).log 2>&1 &
```

Steps 1 to 3 can run at the same time.

## 4. SCP1348 (Slide-TCR-seq) -- needs you in a browser once

1. Open https://singlecell.broadinstitute.org/single_cell/study/SCP1348 and sign in (Google account).
2. Download tab -> Bulk download -> it shows a `curl ... generate_curl_config?...auth_code=XXXXXX ... -o cfg.txt` command. Copy it. The auth code is only valid for about 30 minutes, so do steps 3 and 4 right away.
3. On TACC, generate the config in the right folder (paste the copied command in place of the placeholder, keep `-o cfg.txt`):

```bash
mkdir -p /scratch/10119/ghzheng/spatial_TCR/data/raw/SCP1348 && cd /scratch/10119/ghzheng/spatial_TCR/data/raw/SCP1348 && PASTE_THE_COPIED_CURL_COMMAND_HERE
```

4. Drop the 26 pickle objects (377 GB, redundant with the h5ad files) and start the download:

```bash
cd /scratch/10119/ghzheng/spatial_TCR/data/raw/SCP1348 && python3 ../../../scripts/scp_filter_cfg.py cfg.txt cfg_filtered.txt && nohup curl -K cfg_filtered.txt > ../../../logs/scp1348_$(date +%Y%m%d).log 2>&1 &
```

The filter prints the expiry time of the signed URLs; the download must finish before it (about 24 h, 60 GB is fine).

5. Afterwards, find anything that came back as an XML error instead of data (that is exactly what happened on the old copy):

```bash
cd /scratch/10119/ghzheng/spatial_TCR/data/raw/SCP1348 && find SCP1348 -type f -size -2k -exec sh -c 'head -c 40 "$1" | grep -q "<?xml" && echo "ERROR_PLACEHOLDER $1"' _ {} \;
```

If any are listed, regenerate cfg.txt (step 2 and 3), filter it with `--include` on those filenames, and curl again.

## 5. Brain-metastasis TCR fastqs (optional, later)

GSE179572 has six SRA runs (SRR15052437 to SRR15052442, about 1.3 GB). Not in pass 1; if needed:

```bash
module load sratoolkit 2>/dev/null; cd /scratch/10119/ghzheng/spatial_TCR/data/raw/GSE179572 && for r in SRR15052437 SRR15052438 SRR15052439 SRR15052440 SRR15052441 SRR15052442; do fasterq-dump --split-files -O sra $r || echo "FAILED $r"; done
```

## 6. In situ sequencing TCR (TissUUmaps) -- NOT re-downloadable as of 2026-11-01

The paper publishes no repository. The NSCLC data sit behind https://re0978c72.serve.scilifelab.se
and the PREDIX LumB data behind https://r0928505c.serve.scilifelab.se, both TissUUmaps viewers.
Checked 2026-11-01: both servers answer the h5ad paths (`Clonotypes.h5ad`, `Cell Types.h5ad`,
`Cell types.h5ad`, `TRVbVa pairs.h5ad`) with the viewer's HTML page instead of HDF5 bytes, even
for the viewer's own byte-range requests, and the NSCLC viewer hangs on "Loading markers".
The DAPI images are only served as DeepZoom tiles. So there is nothing for TACC to fetch.

Options: (a) copy the two tar files already on the external drive
(`F:\Tcellworldmodel\In situ sequencing\Raw Data\1.tar`, 11.5 GB, NSCLC; `2.tar`, 1.1 GB, PREDIX)
to TACC with scp; (b) ask the corresponding author (Mats Nilsson's group, SciLifeLab) for the h5ad
files; (c) drop this dataset. Note the tars hold the h5ad files but the TIFF entries are AppleDouble
`._*.tif` sidecars, so the images may be incomplete there too.

If (a):

```bash
scp "F:\Tcellworldmodel\In situ sequencing\Raw Data\1.tar" "F:\Tcellworldmodel\In situ sequencing\Raw Data\2.tar" ghzheng@vista.tacc.utexas.edu:/scratch/10119/ghzheng/spatial_TCR/data/raw/iss_tissuumaps/
```

## 7. After everything lands

Sizes and checksums are in each `provenance.tsv`. `$SCRATCH` is purged; once a dataset is
verified, copy it to Corral (`/corral/utexas/MCB26031/genhui/spatial_TCR_raw/`) before any
processing starts.
