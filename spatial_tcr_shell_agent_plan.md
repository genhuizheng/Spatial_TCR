# Agent Research & Implementation Brief: TCR-Centered Spatial Shell Model

**Date:** 2026-10-31  
**Status:** Exploratory / MVP; hypothesis-generating, not a validated TCR-design pipeline.  
**Primary deliverable:** Download and preprocess suitable **public** spatial-TCR datasets, then produce reproducible **TCR-centered concentric-shell (annular) neighborhood features** and QC visualizations.  
**Do not start by training a large model.**

## 0. What we are actually asking

We want to study TCR clonotypes as the central objects, not spatial spots as the ultimate prediction units.

**Primary scientific question:** Do local cell composition, tumor–stroma boundary positioning, and immune-niche features surrounding a spatially localized TCR carry information about the associated T-cell functional state (activation, exhaustion, possible tumor reactivity) beyond clonotype identity and conventional scRNA/TCR information?

**Longer-term goal (not the MVP):** Test whether these features can improve **context-specific** TCR–peptide–HLA prioritization and ultimately support function-aware TCR selection/design. Do **not** treat local immune context as a direct determinant or experimental label of intrinsic biochemical TCR–pMHC binding.

Key concepts to keep distinct:
- **Molecular recognition**: whether a TCR recognizes a particular peptide–HLA.
- **Tumor reactivity**: whether that TCR recognizes antigens presented by tumor cells.
- **T-cell function/state**: activation, progenitor exhaustion, terminal exhaustion, cytotoxicity, helper function, suppression, etc.
- **Spatial association**: contextual evidence; not proof of antigen specificity or killing.

Analyze CD8, CD4, and (only if properly detected) other T-cell subsets separately or with explicit type covariates. Do not equate CD4 with nonfunctional or all CD8 with killing. Do not infer a TCR sequence itself is “exhausted.”

## 1. First task: public-data audit (mandatory before bulk download)

The user previously collected data on a different drive that is not available now. **Do not assume it is accessible.** Start with these public sources, inspect their actual sample-level files, metadata and linkage, and determine whether they can support the proposed analysis.

| Priority | Dataset / source | Verified public entry point | Why useful | Mandatory verification |
|---|---|---|---|---|
| P0 | McCord et al., *Single-cell TCR mapping reveals spatially coordinated T cell states in head and neck cancer* (Science Immunology, 2026) | Spatial Xenium: [GSE300147](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300147); scRNA: [GSE287301](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE287301); PBMC TCR: [GSE285951](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE285951); [full article](https://pmc.ncbi.nlm.nih.gov/articles/PMC13138865/) | Single-cell spatial localization and patient-specific TCR probes; transcriptional states; matched cohort resources | Which **spatial cells have mapped clonotype IDs**? Can those IDs be linked to actual α/β sequences? Which patients and sections overlap? Does published scRNA accession contain tumor TCR calls or are some TCR data elsewhere? What is accessible? |
| P0/P1 | Beck et al., *High-sensitive spatially resolved T cell receptor sequencing with SPTCR-seq* (Nature Communications, 2023) | Spatial TCR [GSE238071](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE238071); spatial transcriptomics [Dryad](https://doi.org/10.5061/dryad.h70rxwdmj); processed resources [OSF](https://osf.io/65y3t/); [paper](https://www.nature.com/articles/s41467-023-43201-6); [pipeline](https://github.com/theMILOlab/SPTCR-Seq-Pipeline) | Spot-level spatial TCR localization, tumor context, shell-feasibility fallback | Spot-level, not necessarily cell-level, location; sample alignment/coordinate frame; clonotype assignment confidence; whether deconvolution reference is available or must be assembled |
| P1 | Wang group SPACER spatial/TCR resources | [SPACER article](https://www.nature.com/articles/s41551-026-01804-6), which points to **GSE300147** Xenium–TCR, plus other spatial resources | Methodological comparison and possible reuse of the above shared public resource | Avoid counting the same GSE300147 data as an independent validation cohort; distinguish processed results from raw spatial/TCR observations |

**Source-of-truth note:** These accession IDs and links are reported in the publications. That does **not** guarantee every necessary matrix, coordinate, matched chain, or peptide–HLA label is downloadable. Check each file in practice and record what is missing. Some Xenium samples profile only selected, abundant clonotypes with patient-specific probes; they are *not* an unbiased full-repertoire measurement.

Search for other public datasets **only after** auditing the three entries above. Additional datasets must be backed by a paper, an accession, and direct evidence of spatially mapped clonotypes. Plain Visium + separate scTCR from unrelated individuals does **not** qualify as spatial TCR. Report datasets unsuitable for analysis instead of forcing a match.

Produce `data_audit.tsv` with fields: dataset, citation, organism, cancer_type, platform, patient_id, specimen_id, section_id, spatial_resolution, coordinates_unit, TCR_spatial_assignment_type, TCR_alpha_available, TCR_beta_available, paired_alpha_beta_available, clonotype_id_available, cell_expression_available, spatial_expression_available, tumor_annotation_available, histology_available, matched_patient_scRNA_available, matched_pMHC_labels_available, file_url, file_size, license_restrictions, access_status, notes.

**Data download policy:** Prefer processed matrices/tables + coordinates + cell segmentation and TCR assignments before FASTQ. Inspect a small representative sample first. Log SHA256 checksums, provenance and versions. Do not fetch very large raw files without necessity; respect disk quota and avoid silent redundant downloads. Do not invent links, IDs, or sample matches.

## 2. The minimum viable dataset and analysis unit

A qualifying example must have:
1. Coordinates in a known shared tissue frame for **TCR-bearing cell or spot**.
2. A credible spatial mapping to `patient_id`, `section_id`, `tcr_clonotype_id` (or spatially mapped TCR chain/sequence), including ambiguity/confidence where available.
3. Spatial gene-expression and/or cell-type measurements in that tissue, with coordinates and ideally tumor/stroma mask or image.
4. Sufficient TCR-bearing observations to compute neighborhoods and compare regions.

**Unit hierarchy:** `patient -> section -> spatial TCR occurrence (cell/spot) -> clonotype`. The same clonotype may occur in multiple locations; **do not average everything before making shell features**. If a spot contains multiple clonotypes, retain many-to-many assignments and flag uncertainty. Do not assign inferred single-cell coordinates to an unresolved spot.

Store separate identifiers for α chain, β chain, and paired αβ clonotype. Do **not** fabricate pairings from unpaired sequences. Keep TCR and clonotype assignment confidence.

If a dataset lacks direct clonotype coordinates but has a probabilistic TCR-to-location mapping, retain the mapping as weighted/inferred with a distinct `mapping_method`; never call it directly measured.

## 3. Preprocessing (implement first, before modeling)

### 3.1 Ingestion and geometry
- Download and verify sample files; parse relevant formats (`h5ad`, 10x MTX/H5, Xenium tables/parquet, spatial coordinates, TCR AIRR/VDJ tables, images/masks).
- Normalize metadata to a canonical schema. Preserve **raw counts**, original gene identifiers, raw coordinate system, original segmentation ID, original patient/sample IDs, and original TCR calls.
- Calculate QC: cell/spot counts, detected genes, library size, T-cell enrichment, spatial coverage, clonotypes per patient, cells per clonotype, multiple TCRs per spot/cell, unmatched ID rates, low-confidence probe assignment.
- Work in physical µm if a verified pixel-to-µm scale exists; otherwise use native spatial units and explicitly label them. Never mix scales across datasets.
- Match TCR-to-expression by actual matched barcode/cell/spot/region metadata; do not spatially join different samples solely by similar coordinates.

### 3.2 Cell types and deconvolution
- **Single-cell resolution (e.g., Xenium):** prefer observed or confidently inferred cell-type labels and segmentation coordinates; **do not perform redundant spot deconvolution**. If gene panel is limited, optionally transfer labels from matched scRNA with uncertainty estimates.
- **Multicellular spots (e.g., Visium/SPTCR-seq integration):** use a documented deconvolution method such as cell2location or RCTD with an appropriate, ideally patient-matched scRNA reference. Report uncertainty and reference compatibility.
- Core categories: malignant/tumor, normal epithelial, CD8 effector, CD8 progenitor/memory, CD8 exhausted, CD4 helper, Treg, B/plasma, DC, macrophage/monocyte, CAF/fibroblast, endothelial, other/unknown. Use coarse labels if data do not support fine-grained labels. Separate cell type from functional-state labels where possible.
- Distinguish neighbor-cell composition from **the focal TCR-bearing T cell's own expression/state**.

### 3.3 Functional states (exploratory, not ground truth)
- If the focal TCR cell has sufficient gene expression, estimate broad activation/cytotoxic, memory/progenitor, exhaustion-associated and regulatory signatures; report gene coverage and uncertainty.
- Candidate markers to examine rather than hard-code as definitive labels: `PDCD1, TOX, HAVCR2, LAG3, ENTPD1, TCF7, IL7R, SLAMF6, GZMB, PRF1, IFNG, FOXP3`.
- A PD-1-positive cell is not automatically exhausted; transcript signatures are not a killing assay.
- For *later supervised prediction*, avoid leakage: a label computed from the focal cell's genes must not be predicted by simply feeding the same focal-cell genes back as features. Produce a separate **neighbor-only** feature set with focal cell excluded where resolution allows.

## 4. Concentric-shell (2D annular) construction — MVP

For a focal TCR occurrence at coordinate \(x_i\), define shell \(k\) as:

\[
A_k(i)=\{j : r_{k-1} < \|x_j-x_i\|_2 \le r_k\}.
\]

These are **2D concentric annuli**, not true 3D spherical shells unless 3D coordinates are available.

Use **configurable** radii, e.g. `[0, 25, 75, 150] µm` *only if spatial resolution supports them*. For Visium-like spots whose spacing exceeds the inner radius, select radii compatible with spot diameter/spacing; document any empty shells and support sensitivity analyses with alternate radius sets. For a single-cell assay, optionally examine `[0, 20, 50, 100] µm`. The first bin includes nearby cells but **excludes the focal TCR cell** when building neighbor-only features.

For each focal occurrence and shell, compute:
- counts/densities and fractions of cell types; raw neighbor counts and effective tissue-covered area;
- tumor/APC/myeloid/CAF/Treg/T-cell fractions (where labels are supported);
- local diversity and relative immune-vs-tumor enrichment;
- optionally neighbor gene-program summaries (only supported genes; avoid speculative ligand–receptor claims);
- number of mapped spatial TCR occurrences, same-clone and different-clone counts (optional), spatial clone diversity;
- QC: shell cell count, masked tissue fraction, field-of-view edge truncation, deconvolution entropy/uncertainty, TCR mapping confidence.

Use a KD-tree or spatial index for efficient neighbor search. **Do not treat cells beyond tissue edge as missing cells with zero abundance**. Compute valid tissue support when tissue masks exist. Perform patient/section-specific computation; no neighbors may cross sections.

**Aggregation:** Output (a) occurrence-level shell table, (b) clonotype × section × region distributions, and (c) optional clone-level summary (mean, variance, quantiles, tumor/core/boundary/stroma proportions). Do not collapse the clone to one averaged vector too early.

## 5. Boundary-aware extension (high priority)

Construct tumor/stroma segmentation from available histology, malignant-cell annotations, or smoothed tumor-cell probability. Document exactly how the tumor mask is inferred and manually inspect overlays. A high deconvolved tumor fraction alone is **not** guaranteed to define a histological boundary.

For each TCR occurrence, compute:
- `signed_boundary_distance` (tumor side positive, stroma side negative, zero at interface; verify convention);
- region (`tumor_core`, `tumor_side_boundary`, `stroma_side_boundary`, `distant_stroma`, `unknown`);
- per-shell deconvolution split by `tumor_side` and `stroma_side` (orientation-aware annuli);
- tumor-infiltration tendency and clone-region occupancy summaries;
- mask confidence, distance-to-section-edge, and boundary robustness under smoothing/threshold choices.

At a complex tumor interface, keep the signed-distance field and masks rather than imposing a universal left/right side. If no defensible tumor/stroma mask is available, report boundary analysis as **unavailable**, not fabricated.

## 6. Concrete research hypotheses and diagnostics

**H1 Spatial position:** Do particular clonotypes occupy boundary/core/stroma disproportionately, after accounting for tumor fraction, total T-cell density, sampling depth, probe selection and patient?

**H2 Neighborhood:** Are adjacent tumor, APC, CAF, myeloid or Treg populations associated with focal T-cell activation/exhaustion phenotypes after controlling for focal T-cell type and patient?

**H3 Same-clone, different niches:** Within clonotypes observed across multiple regions, are states different in core vs boundary vs immune-rich niches? This is an association, **not** proof that a clone differentiated or migrated from one region to another.

**H4 Predictive incremental value (only if defensible labels exist):** Do neighbor-only shells and boundary features improve held-out prediction over no-spatial baselines? Use patient-held-out validation and, where feasible, clonotype-held-out validation; report potential confounding and limited generalizability.

**No unsupported claims:** Spatial TCR location, exhaustion marker expression and antigen exposure **cannot** alone establish tumor killing or known peptide specificity. If there are no experimentally verified TCR–pMHC or functional labels, do not produce binding AUCs or claim validated TCR design.

## 7. Minimum visual outputs (produce with processed data)

For each selected patient/section:
1. Tissue spatial map annotated with tumor/stroma mask and boundary, plus detected TCRs (clone colors; separate panels for major clones).
2. Example focal TCR neighborhood showing annuli over tissue/segmentation; include a boundary-crossing example where possible.
3. Heatmap: `clonotype × (shell radius × cell type)` or well-supported condensed categories.
4. Boundary distance vs clone abundance / observed focal T-cell state, stratified by patient or T-cell subset.
5. Same-clone example across multiple niches (if actually present) with focal state and neighbor composition.
6. QC figures: spatial cell density, TCR mapping confidence, shells with insufficient coverage, deconvolution uncertainty.

Never label a clone “tumor killing” or “antigen-specific” without independent evidence. Show actual number of patients, sections, clones and cells in every figure caption.

## 8. Simple modeling (optional only after first features are validated)

Start with no-spatial and simple-spatial **baselines**, not a large neural architecture:

- `Baseline 0`: TCR identity/sequence or available paired sequence features (only where meaningful).
- `Baseline 1`: focal T-cell type/state or established scRNA features, clearly separated from any state-derived labels.
- `Baseline 2`: neighbor-only shell composition + boundary features (logistic/ordinal regression, elastic net, random forest, or small MLP).
- `Baseline 3`: TCR features + shells (late concatenation).

Candidate outcome: observed phenotype categories if directly measured; cautiously labeled putative tumor-reactive status only if the source supports such evidence. **Do not pretend public data contain pMHC ground truth if they do not.**

Future recognition model should retain separate heads:
\[
\hat{p}_{bind}=f(TCR, peptide, HLA), \qquad
\hat{p}_{contextual\_function}=g(TCR, peptide, HLA, shells, boundary, cell\ type).
\]

The peptide/HLA predictor is a future extension requiring genuinely linked experimental labels, carefully curated negatives and strict patient/clonotype/antigen splits. This task is primarily **data preprocessing + shell feature generation**.

## 9. Implementation requirements

Implement in Python using `scanpy/anndata`, `pandas`, `numpy`, `scipy.spatial.cKDTree`, `squidpy` and/or `spatialdata` as appropriate; use deconvolution tools only when the assay requires them. Avoid unnecessary dependencies. No hard-coded patient IDs, tissue dimensions or annotation labels. Make all configuration explicit in YAML.

Suggested project layout:

```text
spatial_tcr_shell/
  README.md
  configs/
    datasets.yaml
    shells.yaml
  data/
    raw/                # original files, immutable, not committed
    interim/            # harmonized per-sample files
    processed/          # annotated spatial and TCR data
  metadata/
    data_audit.tsv
    provenance.tsv
    sample_manifest.tsv
  src/
    download.py
    harmonize.py
    annotate_cells.py
    construct_boundary.py
    build_shells.py
    summarize_clones.py
    plot_qc.py
  outputs/
    sample_id/
      tcr_occurrences.parquet
      shell_features.parquet
      boundary_features.parquet
      clonotype_summary.parquet
      qc_summary.json
      figures/
  tests/
  environment.yml
```

Required feature-table keys: `dataset`, `patient_id`, `section_id`, `occurrence_id`, `cell_or_spot_id`, `clonotype_id`, `tcr_sequence_available`, `mapping_method`, `mapping_confidence`, `x`, `y`, `coordinate_unit`, `shell_inner`, `shell_outer`, `neighbor_count`, `effective_area`, `boundary_region`, `signed_boundary_distance`, `mask_quality_flag`, plus cell-type fractions and QC columns.

Add unit tests with synthetic 2D layouts for annulus inclusivity, focal-cell exclusion, boundary-side assignment, tissue-edge truncation, repeated clonotypes and multi-TCR spots. Store per-dataset execution instructions and reproducible package versions. Never overwrite valid cached results unless explicitly requested.

## 10. Execution order and stopping points

**Phase A — Audit:** Confirm files, matching keys, sample coverage, coordinates, true clonotype linkage and practical sizes for GSE300147, GSE287301, GSE285951 and GSE238071/Dryad. Write the audit, identify one feasible specimen. Flag limitations clearly.

**Phase B — Download/ingest:** Download only that specimen's necessary processed files, verify checksums, create harmonized AnnData/TCR mapping tables, produce QC. If the first dataset is unusable, switch to the next rather than inventing mappings.

**Phase C — Shell MVP:** Generate 2–3 configurable distance shells, cell-composition summaries and per-clone distributions. Produce a sample spatial overlay and example shell figure.

**Phase D — Boundary:** Create/verify tumor–stroma mask and signed-distance field; compute tumor-side vs stroma-side annulus features. If annotation is weak, make limitation explicit and still release shell MVP.

**Phase E — Exhaustion descriptive analysis:** Where focal-cell state is actually measurable, relate it to shell/boundary features, stratifying CD4/CD8 and patients. Provide cautious descriptive results; no causal language.

**Phase F — Feasibility report:** Quantify how many real (patient, clone, location) observations are usable and whether future pMHC/functional prediction is supportable. Report exactly which labels are absent and what additional datasets or validation would be needed.

### Definition of done for MVP
- At least **one genuine public spatial-TCR dataset** ingested with verifiable clonotype-to-location linkage.
- A documented, QC-passing shell-feature table with focal observations and patient/section/clonotype IDs intact.
- A figure showing the shells over an actual tissue section, a clone-level heatmap and a data coverage summary.
- Boundary-aware features **if the tissue mask supports them**, otherwise a documented nonfabricated blocker.
- Complete provenance, setup scripts, and a written limitations/next-steps report.

**Agent behavior:** Think critically, verify real public data, and execute a realistic small end-to-end pipeline. Make reasonable implementation decisions, but never silently replace spatial clonotype measurements with inferred nonmatched data. Prefer a smaller truthful reproducible result to an impressive but invalid benchmark.

## 11. References / source pointers

1. Beck et al., 2023, *High-sensitive spatially resolved T cell receptor sequencing with SPTCR-seq*, Nature Communications: https://www.nature.com/articles/s41467-023-43201-6 ; GEO GSE238071.
2. McCord et al., 2026, *Single-cell TCR mapping reveals spatially coordinated T cell states in head and neck cancer*, Science Immunology: https://pmc.ncbi.nlm.nih.gov/articles/PMC13138865/ ; GSE300147, GSE287301, GSE285951 (verify sample overlap and files).
3. SPACER, 2026, Nature Biomedical Engineering: https://www.nature.com/articles/s41551-026-01804-6 ; note the citation of GSE300147 as an overlapping resource, **not** an independent dataset.
