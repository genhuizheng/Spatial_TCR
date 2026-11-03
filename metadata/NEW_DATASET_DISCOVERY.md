# New spatial TCR dataset discovery (2026-11-02)

Scope: findings that are new since `metadata/RAW_DATA_FORMATS.md`. The full table is
`metadata/SPATIAL_TCR_NEW_DATASET_CANDIDATES.tsv`. Existing downloads (GSE300147, GSE287301,
GSE285951, GSE238071, Dryad h70rxwdmj, OSF 8qbdz/65y3t, SCP1348, GSE179572 expression) are not
repeated here.

Constraint: NCBI GEO and PMC return 403 or a browser check to this workstation, so GEO file lists
for new series are not verified yet. They are listed with the TACC dry-run command below, which
downloads nothing.

## Ranked short list

1. **GSE179572 + PRJNA742564 (brain metastases, Visium TCRβ). Tier A, downloaded 2026-11-03 (12/12 FASTQ MD5 OK).**
   This changes an earlier assessment: GSE179572 was treated as expression-only, but its spatial
   TCR reads are deposited separately as BioProject PRJNA742564.
   - The 6 ENA runs (SRR15052437–42) carry sample titles Patient 15, 16, 19, 24, 26, 27, matching
     the 6 Visium samples pt15–pt27 one to one (ENA filereport, checked 2026-11-02).
   - Read structure checked on the local copy: read 1 = 16 nt Visium barcode + 12 nt UMI + poly-T;
     read 2 begins in TRBV framework 3, consistent with the published V-primer enrichment.
   - Join: the TCR library is amplified from the same spatially barcoded cDNA, so the spot barcode
     links TCR, expression and coordinates within the same section by construction.
   - Limits: TRB only; no processed per-spot TCR table is deposited, so CDR3 calls must be
     reproduced with the authors' pipeline (github.com/whhudson/spatialTCR, MiXCR 3.0.13); per-sample
     TCR UMIs ranged 1–1,973 in the preprint, so some samples will be sparse.
   - The F: drive copies are interleaved SRA dumps whose MD5 does not match ENA; use ENA.
   - Matched scRNA/scTCR for the same patients: GSE179373 (Tier C, supports paired-chain lookup).
2. **GSE328481 (lung adenocarcinoma, Stereo-XCR-seq). Tier B, verify file list.**
   Subcellular-capture spatial transcriptome with TCR/BCR enrichment from the same chip; 11 samples.
   The method preprint claims paired chains at single-cell resolution. Promote to Tier A only after
   the GEO file list shows TCR tables with spatial coordinates.
3. **Zenodo 7961605 (Spatial VDJ, tonsil and HER2+ breast cancer). Tier B.**
   One 25.6 GB zip (CC BY 4.0, MD5 published); raw reads are controlled at EGA (EGAS00001007337).
   Same-section by construction, but zip contents are not yet confirmed to include per-spot TCR calls.
4. **GSE296577 (recurrent glioblastoma after oncolytic HSV, Xenium + TCR probes). Tier B.**
   A conference abstract reports Xenium with custom TCR probes; whether the Xenium outputs are in
   GEO is unverified.
5. **GSE280314 / GSE280318 (10x colorectal cancer, Xenium). Tier B, low priority.**
   Public 10x data; TCR detection by Xenium may cover very few clones. Check the Xenium feature list
   for CDR3-like probe names before any large download.

Not promoted: CNGB STT0000123 (access and file types unstated), neuroblastoma COG and pancreatic
CDR3-probe preprints (no accession), FR3AK-seq (abstract only).

## Other facts verified in this pass

- **Slide-TCR-seq unit conversion (SCP1348):** the original paper states "50 pixels (i.e., 32.5 µm)"
  and adjacent beads "within 20 pixels (i.e., 13 µm)", so 0.65 µm per pixel (paper text on F:,
  where the PDF extraction renders µm as "mm").
- **McCord et al. (GSE300147) methods:** no per-cell TCR probe threshold is published; probes were
  accepted if "detected in at least five T cells" and enriched in the T-cell cluster; mismatched
  patients' probes served as negative controls. No author cell annotations or code were released.
  Published spatial parameters: DBSCAN on CD45+ cells, at least 35 cells within 80 µm; neighborhood
  analyses at 15 µm and "five nearest cells within a 15 µm radius".

## TACC dry-run results (2026-11-02, file lists only, nothing downloaded)

| Series | Files | Size | Consequence |
|---|---|---|---|
| GSE328481 | 11 per-chip `.h5ad` | 6.6 GB | small enough to download and inspect for TCR fields |
| GSE296577 | 20 per-sample tar.gz, Seurat RDS, custom panel, README | 402 GB | read panel + README first |
| GSE179373 | expression MTX only on GEO; VDJ FASTQs are in ENA PRJNA743437 (see below) | 0.2 GB | VDJ for pt15, pt16 and two pools (16/26/27): 8 runs, 9.9 GB |
| GSE280314 | 3 Xenium outs zips, gene panel, H&E with alignment CSV | 68 GB | check panel for CDR3 targets first |
| PRJNA742564 | 12 FASTQ (ENA, MD5) | 3.2 GB | downloaded 2026-11-03, all MD5 OK |
| Zenodo 7961605 | 1 zip (MD5) | 25.6 GB | ready when wanted |

Every GEO series again ships a `*_RAW.tar` that repeats the per-sample files; always exclude it.

## Commands (user runs on TACC; nothing here has been run)

List files and sizes only:

```bash
cd /scratch/10119/ghzheng/spatial_TCR && git pull && python3 scripts/geo_download.py --out data/raw --cache data/raw/geo_meta --dry-run GSE328481 GSE296577 GSE179373 GSE280314 2>&1 | tee logs/geo_dryrun_newcandidates_$(date +%Y%m%d).log
```

```bash
cd /scratch/10119/ghzheng/spatial_TCR && python3 scripts/ena_download.py --out data/raw/PRJNA742564 --dry-run PRJNA742564 && python3 scripts/zenodo_download.py 7961605 --out data/raw/zenodo_7961605 --dry-run
```

Download the Tier A reads (3.2 GB, MD5-verified, resumable):

```bash
cd /scratch/10119/ghzheng/spatial_TCR && nohup python3 scripts/ena_download.py --out data/raw/PRJNA742564 PRJNA742564 > logs/ena_PRJNA742564_$(date +%Y%m%d).log 2>&1 &
```

Sources: [STAR Protocols PMC9189629](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9189629/),
[whhudson/spatialTCR](https://github.com/whhudson/spatialTCR),
[OmicsDI GSE328481](https://www.omicsdi.org/dataset/geo/GSE328481),
[OmicsDI GSE296577](https://www.omicsdi.org/dataset/geo/GSE296577),
[Zenodo 7961605](https://zenodo.org/records/7961605),
[Oliveira 2025 PubMed](https://pubmed.ncbi.nlm.nih.gov/40473992/),
[CNGB STT0000123](https://db.cngb.org/stomics/project/STT0000123),
[Stereo-XCR-seq preprint](https://www.biorxiv.org/content/10.1101/2025.01.16.630222.full.pdf).

## Integrity repair (2026-11-02)

Integrity job 1117137 (gzip -t on every file) found 13 files of the correct size whose first
bytes were an NCBI XML error page: 3 in GSE179572, 6 in GSE238071, the GSE287301 cloupe and 4
Xenium files of GSM9054487/88 in GSE300147. `scripts/repair_bad.sh` re-downloaded them with
`--verify-gzip`; all 13 are FIXED. The archives for GSE179572, GSE238071, GSE287301, GSE300147
and geo_meta were rebuilt (job 1117711, all OK).

## Tier A processing: Visium TCR spot calls (2026-11-03)

Published method, reproduced as written (github.com/whhudson/spatialTCR, commit 6347f12):
MiXCR 3.0.13 `analyze shotgun -s hsa --starting-material rna --align "-OsaveOriginalReads=true"
--assemble "--write-alignments"` on read 2, `exportReadsForClones -s`, then spot barcode
(read 1 bases 1-16) and UMI (17-28) joined to each clone read, first read per barcode+UMI counted.

- `scripts/visium_tcr_counts.py` is a Python 3 port of the authors' `combine_counts.py`. Checked
  locally on the authors' own test set (patient 16, 100k reads): identical to their published
  `output_counts.txt` (357 clones, 2,822 UMIs, 0 differing spot-clone cells), also after renaming
  the reads to the ENA naming scheme.
- Why a port: ENA names mates `SRR15052440.1 1/1` and `.1 1/2`; the original pairs mates by
  replacing `1:N:0` with `2:N:0` and would count nothing on the public FASTQs.
- MiXCR `shotgun` calls all chains; in the test set only 197 of 2,822 UMIs are TRB (most are
  IGK), so downstream work filters `chain == TRB`.
- MiXCR 3.0.13 as distributed now (jar rebuilt 2022-07) needs a free academic license key
  (licensing.milaboratories.com), read from `$HOME/mi.license`. Job 1119390 failed for that reason.
- Run order on TACC: `bash scripts/setup_mixcr.sh` (login node), then `sbatch
  scripts/visium_tcr.slurm`; the job runs the authors' test set first and stops unless it
  matches their counts.
- Sample sheet: `metadata/visium_tcr_samples.tsv` (SRR15052437-42 = patients 27, 26, 24, 19, 16,
  15 per ENA sample titles; GSM5420749-54 = pt15, 16, 19, 24, 26, 27).

### Result: job 1119475 (2026-11-03, 3 min on one gg node)

The test sample run on TACC also matched the authors' published counts (357 clones, 2,822
UMIs, `MATCH`), so this installation and the port reproduce the published method. Outputs:
`outputs/visium_tcr/<sample>/spot_clone_{matrix,long}.tsv` and `outputs/visium_tcr/summary.tsv`.

| sample | R2 reads | aligned | clonotypes (TRB) | UMIs on spots | TRB UMIs in tissue | in-tissue spots with TRB / in-tissue spots |
|---|---|---|---|---|---|---|
| pt15 | 509,157 | 9.84% | 334 (57) | 7,383 | 590 | 415 / 2,112 |
| pt16 | 2,057,866 | 5.76% | 925 (248) | 36,376 | 1,982 | 928 / 1,716 |
| pt19 | 348,486 | 0.03% | 4 (2) | 5 | 1 | 1 / 946 |
| pt24 | 754,089 | 3.18% | 204 (87) | 9,392 | 136 | 92 / 1,298 |
| pt26 | 1,130,748 | 0.07% | 23 (14) | 74 | 21 | 19 / 4,342 |
| pt27 | 2,993,934 | 1.37% | 365 (194) | 1,713 | 415 | 275 / 2,152 |

- Usable TRB signal: pt16 > pt15 > pt27 > pt24. pt19 and pt26 have essentially no TCR reads
  (0.03% and 0.07% aligned), so they are not usable for spatial TCR analysis.
- Brain metastasis "pt19" here is unrelated to the McCord HNSCC pilot Patient 19
  (GSE300147, GSM9054481/82); the patient numbers come from different studies.
- Most UMIs are not TRB (e.g. pt16: 2,083 of 36,376), mainly immunoglobulin chains; downstream
  work uses `chain == TRB` only.

## Matched single-cell TCR for the brain metastasis cohort (2026-11-03)

Correction: GSE179373 has no VDJ files on GEO, but its raw reads in ENA (PRJNA743437, checked
with the ENA filereport) include 10x VDJ libraries; sample titles end in [GEX], [CITE] or [VDJ].
VDJ libraries that overlap the Visium patients (`metadata/bm_sctcr_samples.tsv`):

| sample | GSM | patients | cells sorted | runs | GB |
|---|---|---|---|---|---|
| sc_pt15 | GSM5416363 | 15 | PD-1+ CD8 | SRR15034101, SRR15034102 | 1.6 |
| sc_pt16 | GSM5416366 | 16 | PD-1+ CD8 | SRR15034107, SRR15034108 | 4.0 |
| sc_pool1 | GSM5416372 | 16, 26, 27 | all T cells | SRR15034119, SRR15034120 | 2.5 |
| sc_pool2 | GSM5416375 | 16, 26, 27 | all T cells | SRR15034125, SRR15034126 | 1.7 |

Patients 5, 14 and 17 also have VDJ but no Visium. Pooled captures were hashtag-multiplexed
([CITE] libraries, 5.2 GB for the two pools, not downloaded); no hashtag-to-patient table was
found, so pooled clonotypes are attributed to a patient only when their TRB nt CDR3 occurs in
exactly one of the pool's patients' Visium data.

- Assembly: MiXCR 4.7.0 preset `10x-sc-xcr-vdj` (`scripts/sctcr_mixcr.slurm`). Cell Ranger, the
  10x standard and probably the authors' tool (not checked), has no ARM build, and Vista is ARM.
- Linking: `scripts/link_spot_sctcr.py`, exact TRB CDR3 nucleotide identity; amino-acid-only
  matches reported but not used; patient-mismatched pairs are the negative control.
