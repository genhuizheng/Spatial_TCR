# Raw data formats: spatial TCR project

- generated: 2026-11-02 06:17 UTC on `i614-011.vista.tacc.utexas.edu`
- root: `/scratch/10119/ghzheng/spatial_TCR/data/raw`
- python 3.11.15; libraries: h5py 3.16.0, pyarrow 25.0.1, numpy 2.4.6
- missing optional libraries: none
- method: every file is listed; for each dataset and file kind the smallest non-empty file is opened read-only and summarised. Pickles are scanned, never unpickled.
- full per-file inventory: `raw_file_inventory.tsv`

## Overview

| dataset | files | size | file kinds |
|---|---|---|---|
| GSE179572 | 31 | 2.95 GB | 6 |
| GSE238071 | 9 | 70.57 MB | 1 |
| GSE285951 | 62 | 257.20 MB | 1 |
| GSE287301 | 36 | 5.43 GB | 6 |
| GSE300147 | 122 | 55.96 GB | 7 |
| SCP1348 | 204 | 520.75 GB | 65 |
| dryad_h70rxwdmj | 10 | 10.53 GB | 10 |
| geo_meta | 5 | 21.03 KB | 1 |
| osf_65y3t | 20 | 1.14 GB | 12 |
| osf_8qbdz | 8 | 2.97 GB | 3 |

## GSE179572

| kind | n files | total size | example |
|---|---|---|---|
| *all_spatial_images.tar.gz | 1 | 2.76 GB | GSE179572_all_spatial_images.tar.gz |
| *barcodes.tsv.gz | 6 | 72.99 KB | GSM5420751_pt19_barcodes.tsv.gz |
| *features.tsv.gz | 6 | 2.00 MB | GSM5420749_pt15_features.tsv.gz |
| *filtered_feature_bc_matrix.h5 | 6 | 34.24 MB | GSM5420752_filtered_feature_bc_matrix.h5 |
| *matrix.mtx.gz | 6 | 84.09 MB | GSM5420752_pt24_matrix.mtx.gz |
| *spatial.tar.gz | 6 | 67.89 MB | GSM5420751_spatial.tar.gz |

### `*all_spatial_images.tar.gz` (1 file)

inspected: `GSE179572/GSE179572_all_spatial_images.tar.gz` (2.76 GB)

members: 12 files, 3.41 GB uncompressed
first members:
```text
     220 B  all_spatial_images/._pt15.tif
 511.81 MB  all_spatial_images/pt15.tif
     220 B  all_spatial_images/._pt16.tif
 680.25 MB  all_spatial_images/pt16.tif
     333 B  all_spatial_images/._pt27.tif
 578.49 MB  all_spatial_images/pt27.tif
     220 B  all_spatial_images/._pt26.tif
 578.08 MB  all_spatial_images/pt26.tif
     220 B  all_spatial_images/._pt24.tif
 577.40 MB  all_spatial_images/pt24.tif
     312 B  all_spatial_images/._pt19.tif
 486.94 MB  all_spatial_images/pt19.tif
```

### `*barcodes.tsv.gz` (6 files)

inspected: `GSE179572/GSM5420751_pt19_barcodes.tsv.gz` (5.68 KB)

first lines:
```text
AAACCCGAACGAAATC-1
AAACCGTTCGTCCAGG-1
AAAGGCTCTCGCGCCG-1
AAAGTGTGATTTATCT-1
AAAGTTGACTCCCGTA-1
AAATAACCATACGGGA-1
```
line count (decompressed): 946

### `*features.tsv.gz` (6 files)

inspected: `GSE179572/GSM5420749_pt15_features.tsv.gz` (333.44 KB)

delimiter: tab; columns in first line: 3
first lines:
```text
ENSG00000243485	MIR1302-2HG	Gene Expression
ENSG00000237613	FAM138A	Gene Expression
ENSG00000186092	OR4F5	Gene Expression
ENSG00000238009	AL627309.1	Gene Expression
ENSG00000239945	AL627309.3	Gene Expression
ENSG00000239906	AL627309.2	Gene Expression
```
line count (decompressed): 36,601

### `*filtered_feature_bc_matrix.h5` (6 files)

inspected: `GSE179572/GSM5420752_filtered_feature_bc_matrix.h5` (3.24 MB)

10x feature-barcode matrix (.h5):
shape (features x barcodes): (36601, 1298); nnz=1,997,753
first barcodes: ['AAACCGGGTAGGTACC-1', 'AAACGCTGGGCACGAC-1', 'AAACTGCTGGCTCCAA-1']
| feature_type | n features | examples |
|---|---|---|
| Gene Expression | 36,601 | MIR1302-2HG, FAM138A, OR4F5, AL627309.1 |
other feature fields: _all_tag_keys
HDF5 tree (depth <= 3):
```text
matrix/
  barcodes  dataset shape=(1298,) dtype=|S18
  data  dataset shape=(1997753,) dtype=int32
  features/
    _all_tag_keys  dataset shape=(1,) dtype=|S6
    feature_type  dataset shape=(36601,) dtype=|S15
    genome  dataset shape=(36601,) dtype=|S6
    id  dataset shape=(36601,) dtype=|S15
    name  dataset shape=(36601,) dtype=|S17
  indices  dataset shape=(1997753,) dtype=int64
  indptr  dataset shape=(1299,) dtype=int64
  shape  dataset shape=(2,) dtype=int32
```

### `*matrix.mtx.gz` (6 files)

inspected: `GSE179572/GSM5420752_pt24_matrix.mtx.gz` (7.48 MB)

ERROR while inspecting: BadGzipFile: Not a gzipped file (b'<?')

### `*spatial.tar.gz` (6 files)

inspected: `GSE179572/GSM5420751_spatial.tar.gz` (6.84 MB)

members: 6 files, 7.07 MB uncompressed
first members:
```text
   3.78 MB  spatial/tissue_hires_image.png
   1.64 MB  spatial/detected_tissue_image.jpg
 186.88 KB  spatial/tissue_positions_list.csv
   1.11 MB  spatial/aligned_fiducials.jpg
     166 B  spatial/scalefactors_json.json
 352.30 KB  spatial/tissue_lowres_image.png
```
head of `spatial/tissue_positions_list.csv`:
```text
ACGCCTGACACGCGCT-1,0,0,0,1868,2134
TACCGATCCAACACTT-1,0,1,1,1946,2269
ATTAAAGCGGACGAGC-1,0,0,2,2023,2134
GATAAGGGACGATTAG-1,0,1,3,2101,2269
GTGCAAATCACCAATA-1,0,0,4,2179,2134
```
head of `spatial/scalefactors_json.json`:
```text
{"spot_diameter_fullres": 100.87635114630862, "tissue_hires_scalef": 0.13912076, "fiducial_diameter_fullres": 162.95410569788316, "tissue_lowres_scalef": 0.041736227}
```

## GSE238071

| kind | n files | total size | example |
|---|---|---|---|
| *CORRECTED_UMI_CORRRECTED_IGB_TRABDG.csv.gz | 9 | 70.57 MB | GSM7658221_UKF260_SPTCR13_CORRECTED_UMI_CORRRECTED_IGB_TR... |

### `*CORRECTED_UMI_CORRRECTED_IGB_TRABDG.csv.gz` (9 files)

inspected: `GSE238071/GSM7658227_UKF334_SPTCR14_CORRECTED_UMI_CORRRECTED_IGB_TRABDG.csv.gz` (2.65 MB)

ERROR while inspecting: BadGzipFile: Not a gzipped file (b'<?')

## GSE285951

| kind | n files | total size | example |
|---|---|---|---|
| *TRB.tsv.gz | 62 | 257.20 MB | GSM8713803_23059FL-10-01-24.clones_TRB.tsv.gz |

### `*TRB.tsv.gz` (62 files)

inspected: `GSE285951/GSM8713803_23059FL-10-01-24.clones_TRB.tsv.gz` (104.84 KB)

delimiter: tab; columns in first line: 20
first lines:
```text
cloneId	readCount	readFraction	uniqueMoleculeCount	uniqueMoleculeFraction	targetSequences	targetQualities	allVHitsWithScore	allDHitsWithScore	allJHitsWithScore	allCHitsWithScore	allVAlignments	allDAlignments	allJAlignments	allCAlignments	nSeqCDR3	minQualCDR3	aaSeqCDR3	refPoints	isotype
1	555618.0	0.12471770514286741	7341	0.14294337565230936	TGTGCCAGCAGTCTAGGACAGTTCTATGGCTACACCTTC	[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[	TRBV12-4*00(1649)	TRBD1*00(25)	TRBJ1-2*00(437.7)	TRBC1*00(89.9)	350|366|387|0|16|ST362C|131.0	14|19|36|16|21||25.0	24|40|68|23|39||160.0		TGTGCCAGCAGTCTAGGACAGTTCTATGGCTACACCTTC	58	CASSLGQFYGYTF	:::::::::0:-1:16:16:-2:-5:21:23:-4:39:::	
2	424670.0	0.09532424767200037	5035	0.09804112469818521	TGTGCCAGTAGTATCTTCGGGGAGCTGTTTTTT	[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[	TRBV19*00(948)		TRBJ2-2*00(437.2)	TRBC2*00(95.7)	347|361|384|0|14||140.0		27|43|71|17|33||160.0		TGTGCCAGTAGTATCTTCGGGGAGCTGTTTTTT	58	CASSIFGELFF	:::::::::0:-3:14:::::17:-7:33:::	
5	386494.0	0.0867550092536372	4017	0.07821870862216683	TGTGCCAGCAGGGGACTAGTATCAATTGGGACCCAGTACTTC	[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[	TRBV27*00(1638.6)	TRBD2*00(40)	TRBJ2-5*00(408.5)	TRBC2*00(95.8)	347|358|384|0|11||110.0	16|24|48|11|19||40.0	27|40|68|29|42||130.0		TGTGCCAGCAGGGGACTAGTATCAATTGGGACCCAGTACTTC	58	CASRGLVSIGTQYF	:::::::::0:-6:11:11:0:-8:19:29:-7:42:::	
8	240480.0	0.053979737396478794	2532	0.04930290521068619	TGTGCCAGCAGCCACACAGGGGGCGGCACCGGGGAGCTGTTTTTT	[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[	TRBV7-8*00(1665.3)	TRBD1*00(50)	TRBJ2-2*00(467.5)	TRBC2*00(95.6)	350|362|387|0|12||120.0	15|25|36|15|25||50.0	24|43|71|26|45||190.0		TGTGCCAGCAGCCACACAGGGGGCGGCACCGGGGAGCTGTTTTTT	58	CASSHTGGGTGELFF	:::::::::0:-5:12:15:-3:1:25:26:-4:45:::	
10	214413.0	0.04812856551227215	1556	0.030298309837214737	TGTGCAAGTCGCCCACGACAGGGAGAGGCTACAATGAGCAGTTCTTC	[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[	TRBV12-2*00(1016.5)	TRBD1*00(35)	TRBJ2-1*00(468.9)	TRBC2*00(96.4)	347|359|384|0|12||120.0	14|21|36|16|23||35.0	23|42|70|28|47||190.0		TGTGCAAGTCGCCCACGACAGGGAGAGGCTACAATGAGCAGTTCTTC	58	CASRPRQG_GYNEQFF	:::::::::0:-5:12:16:-2:-3:23:28:-3:47:::	
```
line count (decompressed): 1,322

## GSE287301

| kind | n files | total size | example |
|---|---|---|---|
| *.html.gz | 16 | 58.10 MB | GSM8743453_c2p3.html.gz |
| *.tar.gz | 16 | 803.85 MB | GSM8743489_chip2pool16.tar.gz |
| *aggregation.csv.gz | 1 | 570 B | GSE287301_aggregation.csv.gz |
| *filtered_feature_bc_matrix.tar.gz | 1 | 2.75 GB | GSE287301_filtered_feature_bc_matrix.tar.gz |
| *hnscc_scrnaseq.cloupe.gz | 1 | 1.82 GB | GSE287301_hnscc_scrnaseq.cloupe.gz |
| *patient_matrix.txt.gz | 1 | 155 B | GSE287301_patient_matrix.txt.gz |

### `*.html.gz` (16 files)

inspected: `GSE287301/GSM8743453_c2p3.html.gz` (3.24 MB)

HTML page, title: (none)
looks like a 10x Cell Ranger web summary

### `*.tar.gz` (16 files)

inspected: `GSE287301/GSM8743489_chip2pool16.tar.gz` (33.54 MB)

members: 7 files, 172.09 MB uncompressed
first members:
```text
   3.50 MB  chip2pool16/vloupe.vloupe
   7.00 MB  chip2pool16/consensus_annotations.csv
   1.06 MB  chip2pool16/clonotypes.csv
 110.78 MB  chip2pool16/vdj_contig_info.pb
  10.41 MB  chip2pool16/filtered_contig_annotations.csv
  39.08 MB  chip2pool16/airr_rearrangement.tsv
 258.88 KB  chip2pool16/cell_barcodes.json
```
head of `chip2pool16/consensus_annotations.csv`:
```text
clonotype_id,consensus_id,length,chain,v_gene,d_gene,j_gene,c_gene,full_length,productive,fwr1,fwr1_nt,cdr1,cdr1_nt,fwr2,fwr2_nt,cdr2,cdr2_nt,fwr3,fwr3_nt,cdr3,cdr3_nt,fwr4,fwr4_nt,reads,umis,v_start,v_end,v_end_ref,j_start,j_start_ref,j_end,fwr1_start,fwr1_end,cdr1_start,cdr1_end,fwr2_start,fwr2_end,cdr2_start,cdr2_end,fwr3_start,fwr3_end,cdr3_start,cdr3_end,fwr4_start,fwr4_end
sample0_clonotype1,sample0_clonotype1_consensus_1,748,TRB,TRBV13,,TRBJ2-1,TRBC2,true,true,AAGVIQSPRHLIKEKRETATLKCYPI,GCTGCTGGAGTCATCCAGTCCCCAAGACATCTGATCAAAGAAAAGAGGGAAACAGCCACTCTGAAATGCTATCCTATC,PRHDT,CCTAGACACGACACT,VYWYQQGPGQDPQFLIS,GTCTACTGGTACCAGCAGGGTCCAGGTCAGGACCCCCAGTTCCTCATTTCG,FYEKMQ,TTTTATGAAAAGATGCAG,SDKGSIPDRFSAQQFSDYHSELNMSSLELGDSALYF,AGCGATAAAGGAAGCATCCCTGATCGATTCTCAGCTCAACAGTTCAGTG
sample0_clonotype1,sample0_clonotype1_consensus_2,588,TRA,TRAV21,,TRAJ26,TRAC,true,true,KQEVTQIPAALSVPEGENLVLNCSFT,AAACAGGAGGTGACGCAGATTCCTGCAGCTCTGAGTGTCCCAGAAGGAGAAAACTTGGTTCTCAACTGCAGTTTCACT,DSAIYN,GATAGCGCTATTTACAAC,LQWFRQDPGKGLTSLLL,CTCCAGTGGTTTAGGCAGGACCCTGGGAAAGGTCTCACATCTCTGTTGCTT,IQSSQRE,ATTCAGTCAAGTCAGAGAGAG,QTSGRLNASLDKSSGRSTLYIAASQPGDSATYL,CAAACAAGTGGAAGACTTAATGCCTCGCTGGATAAATCATCAGGAC
sample0_clonotype2,sample0_clonotype2_consensus_1,552,TRB,TRBV30,,TRBJ2-7,TRBC2,true,true,SQTIHQWPATLVQPVGSPLSLECTVE,TCTCAGACTATTCATCAATGGCCAGCGACCCTGGTGCAGCCTGTGGGCAGCCCGCTCTCTCTGGAGTGCACTGTGGAG,GTSNPN,GGAACATCAAACCCCAAC,LYWYRQAAGRGLQLLFY,CTATACTGGTACCGACAGGCTGCAGGCAGGGGCCTCCAGCTGCTCTTCTAC,SIGID,TCCATTGGTATTGAC,QISSEVPQNLSASRPQDRQFILSSKKLLLSDSGFYL,CAGATCAGCTCTGAGGTGCCCCAGAATCTCTCAGCCTCCAGACCCCAGG
sample0_clonotype2,sample0_clonotype2_consensus_2,563,TRA,TRAV22,,TRAJ13,TRAC,true,true,GIQVEQSPPDLILQEGANSTLRCNFS,GGAATACAAGTGGAGCAGAGTCCTCCAGACCTGATTCTCCAGGAGGGAGCCAATTCCACGCTGCGGTGCAATTTTTCT,DSVNN,GACTCTGTGAACAAT,LQWFHQNPWGQLINLFY,TTGCAGTGGTTTCATCAAAACCCTTGGGGACAGCTCATCAACCTGTTTTAC,IPSGT,ATTCCCTCAGGGACA,KQNGRLSATTVATERYSLLYISSSQTTDSGVYF,AAACAGAATGGAAGATTAAGCGCCACGACTGTCGCTACGGAACGCTACAGCTTATTGT
```
head of `chip2pool16/clonotypes.csv`:
```text
clonotype_id,frequency,proportion,cdr3s_aa,cdr3s_nt,inkt_evidence,mait_evidence
sample0_clonotype1,89,0.008938435271668174,TRB:CASSSSGGDPYNEQFF;TRA:CAVDNYGQNFVF,TRB:TGTGCCAGCAGCTCTAGCGGGGGGGATCCCTACAATGAGCAGTTCTTC;TRA:TGTGCTGTGGATAACTATGGTCAGAATTTTGTCTTT,,
sample0_clonotype2,53,0.00532288842020689,TRB:CAWSGIRVYEQYF;TRA:CAVPSGGYQKVTF,TRB:TGTGCCTGGAGTGGGATACGGGTGTACGAGCAGTACTTC;TRA:TGTGCTGTGCCTTCTGGGGGTTACCAGAAAGTTACCTTT,,
sample0_clonotype3,51,0.005122024706236818,TRA:CAVPSGGYQKVTF,TRA:TGTGCTGTGCCTTCTGGGGGTTACCAGAAAGTTACCTTT,,
sample0_clonotype4,48,0.004820729135281711,TRB:CASSEGLAGLQETQYF,TRB:TGTGCCAGCAGCGAGGGACTAGCGGGGCTCCAAGAGACCCAGTACTTC,,
```
head of `chip2pool16/filtered_contig_annotations.csv`:
```text
barcode,is_cell,contig_id,high_confidence,length,chain,v_gene,d_gene,j_gene,c_gene,full_length,productive,fwr1,fwr1_nt,cdr1,cdr1_nt,fwr2,fwr2_nt,cdr2,cdr2_nt,fwr3,fwr3_nt,cdr3,cdr3_nt,fwr4,fwr4_nt,reads,umis,raw_clonotype_id,raw_consensus_id,exact_subclonotype_id
AAACCAGCAAACGAGC-1,true,AAACCAGCAAACGAGC-1_contig_1,true,543,TRB,TRBV7-9,,TRBJ2-1,TRBC2,true,true,DTGVSQDPRHKITKRGQNVTFRCDPI,GATACTGGAGTCTCCCAGGACCCCAGACACAAGATCACAAAGAGGGGACAGAATGTAACTTTCAGGTGTGATCCAATT,SEHNR,TCTGAACACAACCGC,LYWYRQTLGQGPEFLTY,CTTTATTGGTACCGACAGACCCTGGGGCAGGGCCCAGAGTTTCTGACTTAC,FQNEAQ,TTCCAGAATGAAGCTCAA,LEKSRLLSDRFSAERPKGSFSTLEIQRTEQGDSAMYL,CTAGAAAAATCAAGGCTGCTCAGTGATCGGTTCTCTGCAG
AAACCAGCACTACGCA-1,true,AAACCAGCACTACGCA-1_contig_1,true,513,TRA,TRAV21,,TRAJ26,TRAC,true,true,KQEVTQIPAALSVPEGENLVLNCSFT,AAACAGGAGGTGACGCAGATTCCTGCAGCTCTGAGTGTCCCAGAAGGAGAAAACTTGGTTCTCAACTGCAGTTTCACT,DSAIYN,GATAGCGCTATTTACAAC,LQWFRQDPGKGLTSLLL,CTCCAGTGGTTTAGGCAGGACCCTGGGAAAGGTCTCACATCTCTGTTGCTT,IQSSQRE,ATTCAGTCAAGTCAGAGAGAG,QTSGRLNASLDKSSGRSTLYIAASQPGDSATYL,CAAACAAGTGGAAGACTTAATGCCTCGCTGGATAAATCA
AAACCAGCACTACGCA-1,true,AAACCAGCACTACGCA-1_contig_2,true,517,TRB,TRBV13,,TRBJ2-1,TRBC2,true,true,AAGVIQSPRHLIKEKRETATLKCYPI,GCTGCTGGAGTCATCCAGTCCCCAAGACATCTGATCAAAGAAAAGAGGGAAACAGCCACTCTGAAATGCTATCCTATC,PRHDT,CCTAGACACGACACT,VYWYQQGPGQDPQFLIS,GTCTACTGGTACCAGCAGGGTCCAGGTCAGGACCCCCAGTTCCTCATTTCG,FYEKMQ,TTTTATGAAAAGATGCAG,SDKGSIPDRFSAQQFSDYHSELNMSSLELGDSALYF,AGCGATAAAGGAAGCATCCCTGATCGATTCTCAGCTCAACAG
AAACCAGCAGCTGTAT-1,true,AAACCAGCAGCTGTAT-1_contig_1,true,498,TRB,TRBV27,,TRBJ2-5,TRBC2,true,true,EAQVTQNPRYLITVTGKKLTVTCSQN,GAAGCCCAAGTGACCCAGAACCCAAGATACCTCATCACAGTGACTGGAAAGAAGTTAACAGTGACTTGTTCTCAGAAT,MNHEY,ATGAACCATGAGTAT,MSWYRQDPGLGLRQIYY,ATGTCCTGGTATCGACAAGACCCAGGGCTGGGCTTAAGGCAGATCTACTAT,SMNVEV,TCAATGAATGTTGAGGTG,TDKGDVPEGYKVSRKEKRNFPLILESPSPNQTSLYF,ACTGATAAGGGAGATGTTCCTGAAGGGTACAAAGTCTCTCGA
```
head of `chip2pool16/airr_rearrangement.tsv`:
```text
cell_id	clone_id	sequence_id	sequence	sequence_aa	productive	rev_comp	v_call	v_cigar	d_call	d_cigar	j_call	j_cigar	c_call	c_cigar	sequence_alignment	germline_alignment	junction	junction_aa	junction_length	junction_aa_length	v_sequence_start	v_sequence_end	d_sequence_start	d_sequence_end	j_sequence_start	j_sequence_end	c_sequence_start	c_sequence_end	consensus_count	duplicate_count	is_cell
AAACCAGCAAACGAGC-1	sample0_clonotype5880	AAACCAGCAAACGAGC-1_contig_1	CAGCAAACAAGCATTAATTACTAGTTTATTATATAGAGACAGTGACCCTGATCTGGTAAAGCTCCCATCCTGCCCTGACCCTGCCATGGGCACCAGCCTCCTCTGCTGGATGGCCCTGTGTCTCCTGGGGGCAGATCACGCAGATACTGGAGTCTCCCAGGACCCCAGACACAAGATCACAAAGAGGGGACAGAATGTAACTTTCAGGTGTGATCCAATTTCTGAACACAACCGCCTTTATTGGTACCGACAGACCCTGGGGCAGGGCCCAGAGTTTCTGACTTACTTCCAGAATGAAGCTCAACTAGAAAAATCAAGGCTGCTCAGTGAT
AAACCAGCACTACGCA-1	sample0_clonotype1	AAACCAGCACTACGCA-1_contig_1	GAGAGTGTTTATCTTGTGAGCCATTCTCCATATTTCAGATATAAGATTTCAGTTCTCAGTGAGTCTAAGTGACAGAAGGAATGGAGACCCTCTTGGGCCTGCTTATCCTTTGGCTGCAGCTGCAATGGGTGAGCAGCAAACAGGAGGTGACGCAGATTCCTGCAGCTCTGAGTGTCCCAGAAGGAGAAAACTTGGTTCTCAACTGCAGTTTCACTGATAGCGCTATTTACAACCTCCAGTGGTTTAGGCAGGACCCTGGGAAAGGTCTCACATCTCTGTTGCTTATTCAGTCAAGTCAGAGAGAGCAAACAAGTGGAAGACTTAATGCCTCGCT
AAACCAGCACTACGCA-1	sample0_clonotype1	AAACCAGCACTACGCA-1_contig_2	GACCCCAGGAGACCAGCAACCTGAGCAGGGAGATGCTTAGTCCTGACCTGCCTGACTCTGCCTGGAACACCAGGCTCCTCTGCCATGTCATGCTTTGTCTCCTGGGAGCAGTTTCAGTGGCTGCTGGAGTCATCCAGTCCCCAAGACATCTGATCAAAGAAAAGAGGGAAACAGCCACTCTGAAATGCTATCCTATCCCTAGACACGACACTGTCTACTGGTACCAGCAGGGTCCAGGTCAGGACCCCCAGTTCCTCATTTCGTTTTATGAAAAGATGCAGAGCGATAAAGGAAGCATCCCTGATCGATTCTCAGCTCAACAGTTCAGTGACTA
AAACCAGCAGCTGTAT-1	sample0_clonotype4	AAACCAGCAGCTGTAT-1_contig_1	ACCTGGAGCCCCCAGAACTGGCAGACACCTGCCTGATGCTGCCATGGGCCCCCAGCTCCTTGGCTATGTGGTCCTTTGCCTTCTAGGAGCAGGCCCCCTGGAAGCCCAAGTGACCCAGAACCCAAGATACCTCATCACAGTGACTGGAAAGAAGTTAACAGTGACTTGTTCTCAGAATATGAACCATGAGTATATGTCCTGGTATCGACAAGACCCAGGGCTGGGCTTAAGGCAGATCTACTATTCAATGAATGTTGAGGTGACTGATAAGGGAGATGTTCCTGAAGGGTACAAAGTCTCTCGAAAAGAGAAGAGGAATTTCCCCCTGATCCTG
```
head of `chip2pool16/cell_barcodes.json`:
```text
[
    "AAACCAGCAAACGAGC-1",
    "AAACCAGCACTACGCA-1",
    "AAACCAGCAGCTGTAT-1",
    "AAACCATTCAAGCCTA-1",
```

### `*aggregation.csv.gz` (1 file)

inspected: `GSE287301/GSE287301_aggregation.csv.gz` (570 B)

delimiter: comma; columns in first line: 2
first lines:
```text
sample_id,molecule_h5
chip1pool3,2f59e1f8-9831-408b-afcc-2c63df66983a/per_sample_outs/chip1pool3/count/sample_molecule_info.h5
chip2pool2,a9d48435-dc14-4c09-9367-30bee05ae33b/per_sample_outs/chip2pool2/count/sample_molecule_info.h5
chip1pool1,3afd615f-a004-4c36-b4c8-dfe8128b703e/per_sample_outs/chip1pool1/count/sample_molecule_info.h5
chip1pool7,05fbb051-da4c-4c77-917c-054de8d6b878/per_sample_outs/chip1pool7/count/sample_molecule_info.h5
chip1pool8,845d9f5a-4992-47c7-a1a7-a155f6098913/per_sample_outs/chip1pool8/count/sample_molecule_info.h5
```
line count (decompressed): 17

### `*filtered_feature_bc_matrix.tar.gz` (1 file)

inspected: `GSE287301/GSE287301_filtered_feature_bc_matrix.tar.gz` (2.75 GB)

members: 3 files, 2.75 GB uncompressed
first members:
```text
   1.79 MB  barcodes.tsv.gz
 342.02 KB  features.tsv.gz
   2.75 GB  matrix.mtx.gz
```
head of `barcodes.tsv.gz`:
```text
AAACCAAAGATGGGGC-1
AAACCAAAGCACCATA-1
AAACCAAAGCCGCAAT-1
AAACCAAAGGCGGATA-1
AAACCAAAGGTCTAGC-1
```
head of `features.tsv.gz`:
```text
ENSG00000290825	DDX11L2	Gene Expression
ENSG00000243485	MIR1302-2HG	Gene Expression
ENSG00000237613	FAM138A	Gene Expression
ENSG00000290826	ENSG00000290826	Gene Expression
ENSG00000186092	OR4F5	Gene Expression
```

### `*hnscc_scrnaseq.cloupe.gz` (1 file)

inspected: `GSE287301/GSE287301_hnscc_scrnaseq.cloupe.gz` (1.82 GB)

binary, first bytes 3c3f786d6c207665

### `*patient_matrix.txt.gz` (1 file)

inspected: `GSE287301/GSE287301_patient_matrix.txt.gz` (155 B)

delimiter: tab; columns in first line: 10
first lines:
```text
""	"pool1"	"pool2"	"pool3"	"pool4"	"pool5"	"pool6"	"pool7"	"pool8"	"pool16"
"hash1"	1	6	3	7	2	4	5	3	7
"hash2"	8	9	10	11	12	13	14	9	13
"hash3"	15	16	18	20	21	19	17	17	19
"hash4"	28	24	27	25	26	23	22	26	24

```
line count (decompressed): 5

## GSE300147

| kind | n files | total size | example |
|---|---|---|---|
| *.tif.gz | 14 | 1.75 GB | GSM9054477_May_6_24_231101.tif.gz |
| *cell_boundaries.parquet.gz | 18 | 109.85 MB | GSM9054481_Sept_11_24_240103_cell_boundaries.parquet.gz |
| *cell_feature_matrix.h5 | 18 | 89.70 MB | GSM9054483_Sept_11_24_240109_cell_feature_matrix.h5 |
| *cells.parquet.gz | 18 | 23.66 MB | GSM9054481_Sept_11_24_240103_cells.parquet.gz |
| *morphology.ome.tif.gz | 18 | 47.17 GB | GSM9054481_Sept_11_24_240103_morphology.ome.tif.gz |
| *nucleus_boundaries.parquet.gz | 18 | 103.99 MB | GSM9054481_Sept_11_24_240103_nucleus_boundaries.parquet.gz |
| *transcripts.parquet.gz | 18 | 6.71 GB | GSM9054483_Sept_11_24_240109_transcripts.parquet.gz |

### `*.tif.gz` (14 files)

inspected: `GSE300147/GSM9054477_May_6_24_231101.tif.gz` (15.29 MB)

TIFF first IFD: width=4458, height=5947, bits_per_sample=8, compression=1, photometric=2, samples_per_pixel=3, bigtiff=False
ImageDescription: ImageJ=1.54g 

### `*cell_boundaries.parquet.gz` (18 files)

inspected: `GSE300147/GSM9054481_Sept_11_24_240103_cell_boundaries.parquet.gz` (2.20 MB)

rows: 587,245; row groups: 1; columns: 4
| column | arrow type |
|---|---|
| cell_id | string |
| vertex_x | float |
| vertex_y | float |
| label_id | int64 |
key-value metadata keys: pandas
first rows:
| cell_id | vertex_x | vertex_y | label_id |
|---|---|---|---|
| aaaagghp-1 | 60.35000228881836 | 19.55000114440918 | 1 |
| aaaagghp-1 | 59.712501525878906 | 19.975000381469727 | 1 |
| aaaagghp-1 | 58.650001525878906 | 19.975000381469727 | 1 |
| aaaagghp-1 | 58.22500228881836 | 20.1875 | 1 |
| aaaagghp-1 | 56.95000076293945 | 21.67500114440918 | 1 |

### `*cell_feature_matrix.h5` (18 files)

inspected: `GSE300147/GSM9054483_Sept_11_24_240109_cell_feature_matrix.h5` (1.39 MB)

10x feature-barcode matrix (.h5):
shape (features x barcodes): (540, 24109); nnz=1,080,342
first barcodes: ['aaacejmb-1', 'aaaddcmn-1', 'aaadoeeo-1']
| feature_type | n features | examples |
|---|---|---|
| Gene Expression | 476 | 240103_CAANRGAQKLVF_TRA, 240103_CAASEEVNSGNTPLVF_TRA, 240... |
| Negative Control Codeword | 41 | NegControlCodeword_0500, NegControlCodeword_0501, NegCont... |
| Negative Control Probe | 20 | NegControlProbe_00042, NegControlProbe_00041, NegControlP... |
| Unassigned Codeword | 3 | UnassignedCodeword_0006, UnassignedCodeword_0037, Unassig... |
other feature fields: _all_tag_keys
HDF5 tree (depth <= 3):
```text
matrix/
  barcodes  dataset shape=(24109,) dtype=|S10
  data  dataset shape=(1080342,) dtype=int32
  features/
    _all_tag_keys  dataset shape=(1,) dtype=|S6
    feature_type  dataset shape=(540,) dtype=|S25
    genome  dataset shape=(540,) dtype=|S7
    id  dataset shape=(540,) dtype=|S30
    name  dataset shape=(540,) dtype=|S30
  indices  dataset shape=(1080342,) dtype=int64
  indptr  dataset shape=(24110,) dtype=int64
  shape  dataset shape=(2,) dtype=int32
```

### `*cells.parquet.gz` (18 files)

inspected: `GSE300147/GSM9054481_Sept_11_24_240103_cells.parquet.gz` (492.74 KB)

rows: 23,496; row groups: 1; columns: 11
| column | arrow type |
|---|---|
| cell_id | string |
| x_centroid | double |
| y_centroid | double |
| transcript_counts | int64 |
| control_probe_counts | int64 |
| control_codeword_counts | int64 |
| unassigned_codeword_counts | int64 |
| deprecated_codeword_counts | int64 |
| total_counts | int64 |
| cell_area | double |
| nucleus_area | double |
key-value metadata keys: pandas
first rows:
| cell_id | x_centroid | y_centroid | transcript_counts | control_probe_counts | control_codeword_counts | unassigned_codeword_counts | deprecated_codeword_counts | total_counts | cell_area | nucleus_area |
|---|---|---|---|---|---|---|---|---|---|---|
| aaaagghp-1 | 61.32327651977539 | 22.05775260925293 | 0 | 0 | 0 | 0 | 0 | 0 | 30.43531360477209 | None |
| aaabjhah-1 | 213.43333435058594 | 465.449462890625 | 122 | 0 | 0 | 0 | 0 | 122 | 35.58312629163265 | 27.590469751507044 |
| aaacpefe-1 | 211.79502868652344 | 446.4398498535156 | 254 | 0 | 0 | 0 | 0 | 254 | 81.64250296354294 | 40.95672023668885 |
| aaadcoba-1 | 176.06109619140625 | 464.0672912597656 | 77 | 0 | 0 | 0 | 0 | 77 | 29.757969830185175 | 18.378594417124987 |
| aaalbhmp-1 | 476.6896057128906 | 275.3332824707031 | 0 | 0 | 0 | 0 | 0 | 0 | 72.83703389391303 | None |

### `*morphology.ome.tif.gz` (18 files)

inspected: `GSE300147/GSM9054481_Sept_11_24_240103_morphology.ome.tif.gz` (1.14 GB)

TIFF first IFD: width=14304, height=17111, bits_per_sample=16, compression=34712, photometric=1, samples_per_pixel=1, x_resolution=1.0, resolution_unit=1, tile_width=1024, tile_length=1024, bigtiff=True
OME Pixels: SizeX=14304, SizeY=17111, SizeZ=11, SizeC=1, SizeT=1, Type=uint16, DimensionOrder=XYZCT, PhysicalSizeX=0.2125, PhysicalSizeXUnit=µm, PhysicalSizeY=0.2125, PhysicalSizeYUnit=µm
OME channels: DAPI
OME images in metadata: 1

### `*nucleus_boundaries.parquet.gz` (18 files)

inspected: `GSE300147/GSM9054481_Sept_11_24_240103_nucleus_boundaries.parquet.gz` (2.05 MB)

rows: 578,808; row groups: 1; columns: 4
| column | arrow type |
|---|---|
| cell_id | string |
| vertex_x | float |
| vertex_y | float |
| label_id | int64 |
key-value metadata keys: pandas
first rows:
| cell_id | vertex_x | vertex_y | label_id |
|---|---|---|---|
| aaabjhah-1 | 212.9250030517578 | 462.4000244140625 | 1 |
| aaabjhah-1 | 211.8625030517578 | 463.0375061035156 | 1 |
| aaabjhah-1 | 210.375 | 463.0375061035156 | 1 |
| aaabjhah-1 | 210.375 | 464.1000061035156 | 1 |
| aaabjhah-1 | 210.16250610351562 | 464.3125 | 1 |

### `*transcripts.parquet.gz` (18 files)

inspected: `GSE300147/GSM9054483_Sept_11_24_240109_transcripts.parquet.gz` (84.54 MB)

rows: 4,832,340; row groups: 5; columns: 11
| column | arrow type |
|---|---|
| transcript_id | uint64 |
| cell_id | string |
| overlaps_nucleus | uint8 |
| feature_name | string |
| x_location | float |
| y_location | float |
| z_location | float |
| qv | float |
| fov_name | string |
| nucleus_distance | float |
| codeword_index | int32 |
key-value metadata keys: pandas
first rows:
| transcript_id | cell_id | overlaps_nucleus | feature_name | x_location | y_location | z_location | qv | fov_name | nucleus_distance | codeword_index |
|---|---|---|---|---|---|---|---|---|---|---|
| 281509336455232 | UNASSIGNED | 0 | SPI1 | 218.7331085205078 | 1607.5882568359375 | 13.169468879699707 | 11.789568901062012 | AD15 | 172.84535217285156 | 209 |
| 281509336457128 | UNASSIGNED | 0 | PMP22 | 45.40699005126953 | 1657.059326171875 | 12.845629692077637 | 40.0 | AD15 | 331.58050537109375 | 158 |
| 281509336479175 | UNASSIGNED | 0 | 240103_CAINNARLMF_TRA | 27.749561309814453 | 1595.000732421875 | 13.143414497375488 | 40.0 | AD15 | 315.6477355957031 | 420 |
| 281509336479176 | UNASSIGNED | 0 | PTPRC | 107.44647979736328 | 1625.2296142578125 | 12.915380477905273 | 22.053714752197266 | AD15 | 262.812744140625 | 345 |
| 281509336481823 | UNASSIGNED | 0 | DERL3 | 206.6145782470703 | 1647.9876708984375 | 13.096420288085938 | 40.0 | AD15 | 213.50106811523438 | 258 |

## SCP1348

| kind | n files | total size | example |
|---|---|---|---|
| *.csv | 1 | 493.77 KB | dfs1_filtered_2020-08-31_Puck_200727_02.csv |
| *.fastq | 1 | 511.91 MB | B10-8_S1_L001_R1_001.fastq |
| *.h5ad | 13 | 56.41 GB | 2020-12-12_Puck_201014_05.h5ad |
| *.xls | 2 | 3.08 MB | Supplementary Table 3.xls |
| *NanoporeTCR_clones.csv | 1 | 30.96 KB | 211105_07_NanoporeTCR_clones.csv |
| *bulk.pdf | 1 | 383.51 KB | Supplementary Figure 5B_bulk.pdf |
| *merged_paired_cloneID.txt | 1 | 14.60 MB | spleen1_merged_paired_cloneID.txt |
| *merged_paired_clones.txt | 1 | 17.32 KB | spleen1_merged_paired_clones.txt |
| *paired_cloneID.txt | 14 | 3.28 GB | B10_12_paired_cloneID.txt |
| *paired_clones.txt | 14 | 28.38 MB | V39_paired_clones.txt |
| *slide_seq.pdf | 1 | 383.49 KB | Supplementary Figure 5B_slide_seq.pdf |
| *submit.h5ad | 2 | 5.62 GB | 2021-09-01_Puck_210731_12_submit.h5ad |
| *tcr_labels_filt_tumor.csv | 8 | 260.79 KB | mel08_tcr_labels_filt_tumor.csv |
| *tcr_labels_filt_tumor_exclusive.csv | 7 | 1.29 MB | mel08_tcr_labels_filt_tumor_exclusive.csv |
| Aggregated_clusterassignments.csv | 1 | 3.11 MB | Aggregated_clusterassignments.csv |
| Aggregated_clusterassignments_pretreatment.csv | 1 | 2.06 MB | Aggregated_clusterassignments_pretreatment.csv |
| ERV_loc_counts.csv | 1 | 874.94 KB | ERV_loc_counts.csv |
| HARLEQUIN*locs.csv | 3 | 163.50 KB | HARLEQUIN_1q24.3_locs.csv |
| Merged_mouse*.fastq.gz | 1 | 782.61 MB | Merged_mouse_spleen2_L001_R1_001.fastq.gz |
| Merged_mouse_spleen_paired_cloneID.txt | 1 | 695.11 MB | Merged_mouse_spleen_paired_cloneID.txt |
| Merged_mouse_spleen_paired_clones.txt | 1 | 89.82 KB | Merged_mouse_spleen_paired_clones.txt |
| Puck*NanoporeTCR_BC_UMI_reads.csv | 1 | 2.98 MB | Puck_211105_07_NanoporeTCR_BC_UMI_reads.csv |
| Puck*barcode_matching.txt | 11 | 33.14 MB | Puck_220408_15_barcode_matching.txt |
| Puck*cell_clones.csv | 11 | 91.09 MB | Puck_220408_08_cell_clones.csv |
| Puck*clone_bcumi.csv | 5 | 70.29 MB | Puck_220408_14_clone_bcumi.csv |
| Puck*clones.txt | 5 | 3.41 MB | Puck_220420_17_clones.txt |
| Puck*expression.txt | 7 | 14.85 GB | Puck_200727_02.digital_expression.txt |
| Puck*genenames_barcodes.csv | 2 | 2.37 MB | Puck_200727_02_genenames_barcodes.csv |
| Puck*matched_bead_barcodes.txt | 10 | 4.93 MB | Puck_220408_15_matched_bead_barcodes.txt |
| Puck*matched_bead_locations.txt | 10 | 5.14 MB | Puck_220408_15_matched_bead_locations.txt |
| Puck*sparse_matrix.npz | 2 | 39.54 MB | Puck_200727_02_sparse_matrix.npz |
| Puck_object*.pickle | 17 | 321.76 GB | Puck_object_2020-12-12_Puck_201014_05.pickle |
| Puck_object*submit.pickle | 5 | 100.67 GB | Puck_object_2021-09-01_Puck_210731_11_submit.pickle |
| RCC_Bulk*.xls | 1 | 2.85 MB | RCC_Bulk_TCR.26Oct20.xls |
| Supplementary_Table*.xls | 1 | 222.21 KB | Supplementary_Table_3.xls |
| TCR_de.pdf | 1 | 425.34 KB | TCR_de.pdf |
| adata_erv_rcc*.h5ad | 1 | 4.74 MB | adata_erv_rcc_08.h5ad |
| barcodes.csv | 1 | 164.86 KB | barcodes.csv |
| celltype.csv | 1 | 65.22 KB | celltype.csv |
| cfg*.txt | 1 | 128.05 KB | cfg_20261101_2038.txt |
| cfg.txt | 1 | 128.05 KB | cfg.txt |
| cloneids_readids*.pickle | 1 | 717.76 MB | cloneids_readids_2020-08-31_Puck_200727_02.pickle |
| dge.csv | 1 | 290.10 MB | dge.csv |
| file_supplemental_info.tsv | 1 | 10.66 KB | file_supplemental_info.tsv |
| genes.csv | 1 | 119.71 KB | genes.csv |
| lymph_rctd.csv | 1 | 7.69 MB | lymph_rctd.csv |
| mel_mtx.mtx | 1 | 262.35 MB | mel_mtx.mtx |
| mel_ref.h5ad | 1 | 302.34 MB | mel_ref.h5ad |
| monocyte_de_genes.csv | 1 | 329.59 KB | monocyte_de_genes.csv |
| nUMI.csv | 1 | 49.35 KB | nUMI.csv |
| new_format*.h5ad | 3 | 12.46 GB | new_format_2020-09-02_Puck_200727_10.h5ad |
| post_treatment_clonotype_fraction_slide_seq.csv | 1 | 61.57 KB | post_treatment_clonotype_fraction_slide_seq.csv |
| pre_treatment_clonotype_fraction_slide_seq.csv | 1 | 1.99 KB | pre_treatment_clonotype_fraction_slide_seq.csv |
| rcc*five_cells.csv | 1 | 287.08 KB | rcc_08_five_cells.csv |
| rcc*harl.csv | 1 | 388.35 KB | rcc_08_harl.csv |
| rcc*rcc_cells.csv | 5 | 3.22 MB | rcc_10_rcc_cells.csv |
| rcc_rctd_clusters*.csv | 5 | 3.26 MB | rcc_rctd_clusters_2020-09-02_Puck_200727_12.csv |
| readIDtobarcode_dict*.pickle | 1 | 1.71 GB | readIDtobarcode_dict_2020-08-31_Puck_200727_02.pickle |
| rln_paired_cloneID.txt | 1 | 85.93 MB | rln_paired_cloneID.txt |
| rln_paired_clones.txt | 1 | 1.71 MB | rln_paired_clones.txt |
| spleen_rctd_clusters_aging.csv | 1 | 313.76 KB | spleen_rctd_clusters_aging.csv |
| tcr_de_genes.csv | 1 | 288.98 KB | tcr_de_genes.csv |
| tcr_loc_dict*.pickle | 1 | 654.57 KB | tcr_loc_dict_s1_2020-08-31_Puck_200727_02.pickle |
| trac*.pickle | 1 | 3.33 MB | trac_trbc2_constant_umis_2020-08-31_Puck_200727_02.pickle |
| tumor_proximity_de_genes.csv | 1 | 427.45 KB | tumor_proximity_de_genes.csv |

### `*.csv` (1 file)

inspected: `SCP1348/SCP1348/other/dfs1_filtered_2020-08-31_Puck_200727_02.csv` (493.77 KB)

delimiter: comma; columns in first line: 5
first lines:
```text
x,y,tcr_a,tcr_b,bead_barcodes
2615.5,1946.2,[''],['CASSRANYEQYF'],GTCGGCGAACGACG
3414.9,3290.5,[''],['CASSRANYEQYF'],TACTCAACTGCACA
2474.9,1296.0,[''],['CASSRANYEQYF'],AGGCAGCGAATACA
1861.6,1814.3,[''],['CASSRANYEQYF'],TGTTATAGCACGCG
3215.3,1236.2,[''],['CASSRANYEQYF'],GCCCAAAGCGTAAG
```
line count: 8,803

### `*.fastq` (1 file)

inspected: `SCP1348/SCP1348/fastq/B10-8_S1_L001_R1_001.fastq` (511.91 MB)

first two reads:
```text
@M05522:217:000000000-J63G8:1:1101:18329:1881 1:N:0:1
TTTTGCGGTCTTCAGCGTTCCCGAGAGGCCATGAGTCAGGCTTTTTTT
+
1AAA1111>AAFF31B?EEFFGA0A0A00A/B111FF1AGHHHHHHGG
@M05522:217:000000000-J63G8:1:1101:17794:1912 1:N:0:1
TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
+
1111111100000////A/>EEEEEEGEEGCCCGGGGGGGGGGGGGGG
```

### `*.h5ad` (13 files)

inspected: `SCP1348/SCP1348/anndata/2020-12-12_Puck_201014_05.h5ad` (2.43 GB)

AnnData (.h5ad) summary:
X: dense, shape=(23720, 5347), dtype=float32
obs: 23720 rows, 6 columns; index '_index' (first ids: ['AACAGCTTGTTAAG', 'AAAGCCAGAATGAC', 'TCAAGCCCCACCAG'])
| column | dtype | first values |
|---|---|---|
| n_genes | int64 | [3654, 3242, 3091] |
| n_genes_by_counts | int64 | [3646, 3239, 3086] |
| total_counts | float32 | [8304.0, 6683.0, 6322.0] |
| total_counts_mt | float32 | [117.0, 74.0, 66.0] |
| pct_counts_mt | float32 | [1.4089595079421997, 1.1072871685028076, 1.043973445892334] |
| leiden | categorical (11 levels: 0, 1, 2, 3, 4, 5, 6, 7) | 10, 10, 10 |
var: 5347 rows, 12 columns; index '_index' (first ids: ['A2M', 'A4GALT', 'AACS'])
| column | dtype | first values |
|---|---|---|
| n_cells | int64 | [279, 111, 159] |
| mt | bool | [False, False, False] |
| n_cells_by_counts | int64 | [279, 111, 159] |
| mean_counts | float32 | [0.012536720372736454, 0.004634035285562277, 0.0067028012... |
| pct_dropout_by_counts | float64 | [98.84562869791881, 99.54073399809673, 99.3421324837602] |
| total_counts | float32 | [303.0, 112.0, 162.0] |
| highly_variable | bool | [True, True, True] |
| means | float64 | [0.2454796175369385, 0.07505289570721364, 0.1207074247506... |
| dispersions | float64 | [3.9007456129420497, 3.8838882755010156, 3.964793764486439] |
| dispersions_norm | float32 | [0.6098095178604126, 0.5775893330574036, 0.7322275042533875] |
| mean | float64 | [-1.3742112188676959e-12, -7.9305675760729e-12, 3.4531964... |
| std | float64 | [0.3226181787014608, 0.17664496715440559, 0.2217567535238... |
obsm: X_pca (23720, 50); X_umap (23720, 2)
varm: PCs (5347, 50)
obsp: connectivities (group); distances (group)
uns keys (7): hvg, leiden, leiden_colors, neighbors, pca, rank_genes_groups, umap
HDF5 tree (depth <= 3):
```text
X  dataset shape=(23720, 5347) dtype=float32
obs/ [dataframe]
  __categories/
    leiden  dataset shape=(11,) dtype=object
  _index  dataset shape=(23720,) dtype=object
  leiden  dataset shape=(23720,) dtype=int8
  n_genes  dataset shape=(23720,) dtype=int64
  n_genes_by_counts  dataset shape=(23720,) dtype=int64
  pct_counts_mt  dataset shape=(23720,) dtype=float32
  total_counts  dataset shape=(23720,) dtype=float32
  total_counts_mt  dataset shape=(23720,) dtype=float32
obsm/
  X_pca  dataset shape=(23720, 50) dtype=float32
  X_umap  dataset shape=(23720, 2) dtype=float32
obsp/
  connectivities/ [csr_matrix]
    data  dataset shape=(413934,) dtype=float32
    indices  dataset shape=(413934,) dtype=int32
    indptr  dataset shape=(23721,) dtype=int32
  distances/ [csr_matrix]
    data  dataset shape=(213480,) dtype=float64
    indices  dataset shape=(213480,) dtype=int32
    indptr  dataset shape=(23721,) dtype=int32
raw/ [raw]
  X  dataset shape=(23720, 19949) dtype=float32
  var/ [dataframe]
    _index  dataset shape=(19949,) dtype=object
    dispersions  dataset shape=(19949,) dtype=float64
    dispersions_norm  dataset shape=(19949,) dtype=float32
    highly_variable  dataset shape=(19949,) dtype=bool
    mean_counts  dataset shape=(19949,) dtype=float32
    means  dataset shape=(19949,) dtype=float64
    mt  dataset shape=(19949,) dtype=bool
    n_cells  dataset shape=(19949,) dtype=int64
    n_cells_by_counts  dataset shape=(19949,) dtype=int64
    pct_dropout_by_counts  dataset shape=(19949,) dtype=float64
    total_counts  dataset shape=(19949,) dtype=float32
uns/
  hvg/
    flavor  dataset shape=() dtype=object
  leiden/
    params/
  leiden_colors  dataset shape=(11,) dtype=object
  neighbors/
    connectivities_key  dataset shape=() dtype=object
    distances_key  dataset shape=() dtype=object
    params/
  pca/
    params/
    variance  dataset shape=(50,) dtype=float32
    variance_ratio  dataset shape=(50,) dtype=float32
  rank_genes_groups/
    logfoldchanges  dataset shape=(19949,) dtype=[('0', '<f4'), ('1', '<f4'), ('2', '<f4'), ('3', '<f4'), ('4', '<f4'), ('5', '<f4'), ('6', '<f4'), ('7', '<f4'), ('8', '<f4'), ('9', '<f4'), ('10', '<f4')]
    names  dataset shape=(19949,) dtype=[('0', 'O'), ('1', 'O'), ('2', 'O'), ('3', 'O'), ('4', 'O'), ('5', 'O'), ('6', 'O'), ('7', 'O'), ('8', 'O'), ('9', 'O'), ('10', 'O')]
    params/
    pvals  dataset shape=(19949,) dtype=[('0', '<f8'), ('1', '<f8'), ('2', '<f8'), ('3', '<f8'), ('4', '<f8'), ('5', '<f8'), ('6', '<f8'), ('7', '<f8'), ('8', '<f8'), ('9', '<f8'), ('10', '<f8')]
    pvals_adj  dataset shape=(19949,) dtype=[('0', '<f8'), ('1', '<f8'), ('2', '<f8'), ('3', '<f8'), ('4', '<f8'), ('5', '<f8'), ('6', '<f8'), ('7', '<f8'), ('8', '<f8'), ('9', '<f8'), ('10', '<f8')]
    scores  dataset shape=(19949,) dtype=[('0', '<f4'), ('1', '<f4'), ('2', '<f4'), ('3', '<f4'), ('4', '<f4'), ('5', '<f4'), ('6', '<f4'), ('7', '<f4'), ('8', '<f4'), ('9', '<f4'), ('10', '<f4')]
  umap/
    params/
var/ [dataframe]
  _index  dataset shape=(5347,) dtype=object
  dispersions  dataset shape=(5347,) dtype=float64
  dispersions_norm  dataset shape=(5347,) dtype=float32
  highly_variable  dataset shape=(5347,) dtype=bool
  mean  dataset shape=(5347,) dtype=float64
  mean_counts  dataset shape=(5347,) dtype=float32
  means  dataset shape=(5347,) dtype=float64
  mt  dataset shape=(5347,) dtype=bool
  n_cells  dataset shape=(5347,) dtype=int64
  n_cells_by_counts  dataset shape=(5347,) dtype=int64
  pct_dropout_by_counts  dataset shape=(5347,) dtype=float64
  std  dataset shape=(5347,) dtype=float64
  total_counts  dataset shape=(5347,) dtype=float32
varm/
  PCs  dataset shape=(5347, 50) dtype=float64
```

### `*.xls` (2 files)

inspected: `SCP1348/SCP1348/other/Supplementary Table 3.xls` (222.21 KB)

binary: OLE2 (legacy Excel .xls / Office)

### `*NanoporeTCR_clones.csv` (1 file)

inspected: `SCP1348/SCP1348/other/211105_07_NanoporeTCR_clones.csv` (30.96 KB)

delimiter: comma; columns in first line: 29
first lines:
```text
,cloneId,cloneCount,cloneFraction,targetSequences,targetQualities,allVHitsWithScore,allDHitsWithScore,allJHitsWithScore,allCHitsWithScore,allVAlignments,allDAlignments,allJAlignments,allCAlignments,nSeqImputedFR1,minQualFR1,nSeqImputedCDR1,minQualCDR1,nSeqImputedFR2,minQualFR2,nSeqImputedCDR2,minQualCDR2,nSeqImputedFR3,minQualFR3,nSeqImputedCDR3,minQualCDR3,nSeqImputedFR4,minQualFR4,aaSeqImputedFR
0,0,55677.0,0.737424174194061,TGTGCCAGCTCTCGGGCCAATTATGAACAGTACTTC,{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{,TRBV13*00(224.9),TRBD2*00(25),TRBJ2-7*00(110.9),TRBC1*00(24),270|279|307|0|9||45.0,29|34|48|13|18||25.0,24|39|67|21|36|SC26TSG29A|47.0,,gctgctggagtcatccagtccccaagacatctgatcaaagaaaagagggaaacagccactctgaaatgctatcctatc,,cctagacacgacact,,gtctactggtaccagcagggtccaggtcaggacccccagttcctcatttcg,,ttttatgaaa
1,1,13941.0,0.1846441153876718,TGTGCAGCAAGTGACAACTATCAGTTGATCTGG,{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{,TRAV23DV6*00(198.8),,TRAJ33*00(215),TRAC*00(55.6),267|278|300|0|11||55.0,,27|46|77|14|33|SA39G|81.0,,cagcagcaggtgaaacaaagtcctcaatctttgatagtccagaaaggagggatttcaattataaactgtgcttatgag,,aacactgcgtttgactac,,tttccatggtaccaacaattccctgggaaaggccctgcattattgatagcc,,atacgtccagatgtgagtgaa,,aagaaagaaggaagattcacaatc
2,2,3171.0,0.0419988874466901,TGTGCCAGCTCTGGGCCAATTATGAACAGTACTTC,{{{{{{{{[{`{JIJJ{{{{{W{{{{{{{{b{{\M,TRBV13*00(217.7),TRBD2*00(25),TRBJ2-7*00(106.5),TRBC1*00(19.5),270|279|307|0|9||45.0,29|34|48|12|17||25.0,24|39|67|20|35|SC26TSG29A|47.0,,gctgctggagtcatccagtccccaagacatctgatcaaagaaaagagggaaacagccactctgaaatgctatcctatc,,cctagacacgacact,,gtctactggtaccagcagggtccaggtcaggacccccagttcctcatttcg,,ttttatgaaa
3,3,981.0,0.0129930332971312,TGTGCAGCAAGTGACAACTATCAGTTGATCTG,{{{{{{{{[X{R_{{{{{{{{R{R{{Y{{NON,TRAV23DV6*00(188.7),,TRAJ33*00(196.2),TRAC*00(54.5),267|278|300|0|11||55.0,,27|46|77|14|32|SA39GDG45|64.0,,cagcagcaggtgaaacaaagtcctcaatctttgatagtccagaaaggagggatttcaattataaactgtgcttatgag,,aacactgcgtttgactac,,tttccatggtaccaacaattccctgggaaaggccctgcattattgatagcc,,atacgtccagatgtgagtgaa,,aagaaagaaggaagattcacaa
4,4,308.0,0.0040793621361023,TGTGCCAGCTCTGGGCCAATTATGAACAGTACTTG,T{{a{{{{S{PTFFGHNROMVN{R{Q{{{{MKUK;,TRBV13*00(212.4),TRBD2*00(25),TRBJ2-7*00(89),TRBC1*00(12.9),270|279|307|0|9||45.0,29|34|48|12|17||25.0,24|39|67|20|35|SC26TSG29ASC38G|33.0,,gctgctggagtcatccagtccccaagacatctgatcaaagaaaagagggaaacagccactctgaaatgctatcctatc,,cctagacacgacact,,gtctactggtaccagcagggtccaggtcaggacccccagttcctcatttcg,,ttttatgaa
```
line count: 42

### `*bulk.pdf` (1 file)

inspected: `SCP1348/SCP1348/other/Supplementary Figure 5B_bulk.pdf` (383.51 KB)

binary: PDF

### `*merged_paired_cloneID.txt` (1 file)

inspected: `SCP1348/SCP1348/other/spleen1_merged_paired_cloneID.txt` (14.60 MB)

delimiter: tab; columns in first line: 7
first lines:
```text
descrsR1	cloneId	readId	targetSequences	topChains	chains	cloneMapping
M00158:188:000000000-K3KRB:1:1102:14955:2795 2:Y:0:TAAGTGGC	-1	295	CCCAGCAGATTCTCAGTCCAACAATTTGATGACTATCACTCTGAAATGAACATGAGTGCCTCGGAACTCGCTTCCTCTGCTCTGTCCTTCTGTGCCAGCCCTCCGGCCCCATCACACCTTCCCCCTCTCACCACAAAAAAAACACAAAAAAAAAACAACCAAAAAAAACAAAACAACACCCCACCCCCCGACCCCCCCCCCCCCCCCACCGGCCCACCCACCACCCCGCCGCCCCCCCGCCGACCACC	TRB	TRB	-1:dropped
M00850:271:000000000-K4CVY:1:2107:2167:18183 2:N:0:TAAGTGGC	-1	2226443	CCCAGCAGATTCTCAGTCCAACAGTTTGATGACTATCACTCTGAAATGAACATGAGTGCCTTGGAACTGGAGGACTCTGCTATGTACTTCCGTGCCAGCTCTCGGGCCAATGATGAACGGGGCTTCGGTCCCGGCACCAGGGGCACGGGTTGAGAGGATCTGAGAAATGGGACTCCACCCAAGGGCTCCTTGTTTGAGCCATGGAAGGCAGAGATTGCAAACAAACAAAAGGCTACCCTCGGGTGCTT	TRB	TRB	-1:dropped
M00158:188:000000000-K3KRB:1:1102:20808:3124 2:N:0:TAAGTGGC	-1	440	CCCAGCAGATTCTCAGTCCACCAGCTTGATGACTATCACTCTCACATGAACATGAGCGCCTCGGAACTGCCGGACTCTGCTATTTACTTCTGTGCCACCTCTCGGGCCAACCCTGCTCCGCACCCCGGCCCCTGCACCTGGCTCTCGGTTTTTGGCAAGATCCACATCCCTCCCCCCCACCCACATTCCTGCCCCCCCGGAGTAGCTCGGAGCAGACCAGGGTCAGGGAATCCCCGGGAGGGGCACCG	TRB	TRB	-1:dropped
M00850:271:000000000-K4CVY:1:2107:24273:18184 2:Y:0:TAAGTGGC	-1	2226448	GCCAGCAGATGATCAGTCAAAAAGCTTGATGACTATCACTCGGAAATGAAGATGAGTAAGATGGAACTGGAGGACTCTGCTATGGACTTCTGTGACAGGTCGCGGGCGAAGAAGGAACAGAGCTTCGGGACGGGGGGCAGGGGGAGGGGTTTAGGGGGTCGGGGGGATGGGAGTCCGGAGAAGGGTAGAGAGTTGGGGGGATGGGAGGGGGGGGTGGGGAGCGAAAAAAGGGTGAGCCTGGGGGGGTT	TRB	TRB	-1:dropped
M00158:188:000000000-K3KRB:1:1102:19339:4136 2:N:0:TAAGTGGC	-1	979	CCCAGCAGATTCTCAGTCCAACAGAATGAAGACTATCACTCTTAAATTAACATGATTGTTTTGGAACTGGAGGACTCTGCTATGTACTTCTGTGCCAGCCCTCGGGCCAATCATGAACAGCACCTCGGCCCCGGCACCAGGCACACGGAATTAGAGGAACCTAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAA	TRB	TRB	-1:dropped
```
line count: 43,253

### `*merged_paired_clones.txt` (1 file)

inspected: `SCP1348/SCP1348/other/spleen1_merged_paired_clones.txt` (17.32 KB)

delimiter: tab; columns in first line: 28
first lines:
```text
cloneId	cloneCount	cloneFraction	targetSequences	targetQualities	allVHitsWithScore	allDHitsWithScore	allJHitsWithScore	allCHitsWithScore	allVAlignments	allDAlignments	allJAlignments	allCAlignments	nSeqImputedFR1	minQualFR1	nSeqImputedCDR1	minQualCDR1	nSeqImputedFR2	minQualFR2	nSeqImputedCDR2	minQualCDR2	nSeqImputedFR3	minQualFR3	nSeqImputedCDR3	minQualCDR3	nSeqImputedFR4	minQualFR4	aaSeqImputedFR1
0	12768.0	0.7824008824070102	TGTGCCAGCTCTCGGGCCAATTATGAACAGTACTTC	HHHHHHHHGHHHHGGGGGGHHHHHHHHHHHHHHHHH	TRBV12-1*00(480.7)		TRBJ2-7*00(208.5)	TRBC2*00(211.9),TRBC1*00(206.3)	270|283|305|0|13||65.0		24|39|67|21|36||75.0	;	gattctggggttgtccagtctccaagacacataatcaaagaaaagggaggaaggtccgttctgacgtgtattcccatc		tctggacatagcaat		gtggtctggtaccagcagactctggggaaggaattaaagttccttattcag		cattatgaaaaggtggag		agagacaaag
1	2599.0	0.15926220969422145	TGTGCAGCAAGTGACAACTATCAGTTGATCTGG	HHHHHHHHHHHHHHHHHHHHHHHIIIHHHHHHH	TRAV14N-2*00(347.4),TRAV14N-1*00(346.8),TRAV14D-2*00(346.7),TRAV14D-1*00(345.2)		TRAJ33*00(239.7)	TRAC*00(333.2)	267|280|300|0|13||65.0;267|280|300|0|13||65.0;267|280|300|0|13||65.0;267|280|300|0|13||65.0		27|46|77|14|33||95.0		cagcagcaggtgagacaaagtccccaatctctgacagtctgggaaggagagacagcaattctgaactgcagttat
2	637.0	0.03903425454991115	TGAGCCAGCTCTCGGGCCAATTATGAACAGTACTTC	GHHFGHHHGHFHHGGGGGGHHHHHHHHHHHGHGHHH	TRBV12-1*00(401.4)		TRBJ2-7*00(199.2)	TRBC2*00(131.3),TRBC1*00(124.3)	270|283|305|0|13|ST272A|51.0		24|39|67|21|36||75.0	;	gattctggggttgtccagtctccaagacacataatcaaagaaaagggaggaaggtccgttctgacgtgtattcccatc		tctggacatagcaat		gtggtctggtaccagcagactctggggaaggaattaaagttccttattcag		cattatgaaaaggtggag		agaga
3	153.0	0.009375574483730621	TGAGCAGCAAGTGACAACTATCAGTTGATCTGG	HHHHHHHHHHGGGHHHHHGHHGHHGGGHFFFHH	TRAV14N-1*00(265.3),TRAV14D-2*00(262.7),TRAV14N-2*00(262.7),TRAV14D-1*00(251.5)		TRAJ33*00(242.7)	TRAC*00(227.2)	267|280|300|0|13|ST269A|51.0;267|280|300|0|13|ST269A|51.0;267|280|300|0|13|ST269A|51.0;267|280|300|0|13|ST269A|51.0		27|46|77|14|33||95.0		cagcagcaggtgagacaaagtccccaatctctgacagtctgggaaggagag
4	102.0	0.006250382989153747	TGTGCTATGAGAGAGGGCGAGGGATACGAGAGGGTTACCAGAACTTCTATTTT	HHHHHHHHHHHHHGFFGGGGGGGGHHHGGFGGGGEHHHHHHHHHHHHHHHHHH	TRAV16N*00(354.8),TRAV16D-DV11*00(322.1)		TRAJ49*00(259.1)		273|291|310|0|18||90.0;273|291|310|0|18||90.0		26|48|79|31|53||110.0		gcccagaaggtaacacagactcagacttcaatttctgtgatggagaagacaacggtgacaatggactgtgtgtatgaa		acccgggacagttcttacttc		ttattctggtacaagcaaacagcaagtggg
```
line count: 22

### `*paired_cloneID.txt` (14 files)

inspected: `SCP1348/SCP1348/other/B10_12_paired_cloneID.txt` (22.56 MB)

delimiter: tab; columns in first line: 8
first lines:
```text
descrsR2	descrsR1	cloneId	readId	targetSequences	topChains	chains	cloneMapping
M05522:218:000000000-C5JTY:1:1101:15533:2222 2:N:0:1	M05522:218:000000000-C5JTY:1:1101:15533:2222 1:N:0:1	-1	212	TGCAGCTACTCAACCTGGAACTCAGAGGTCATGATGAGGGTCCAAAAGGCAAGAACTAAATGTGCCCGAAAGTCCAGATCGAAAGAAAAGAAAAAGGAGAAAGATATCTGTTCAAGCTCAAAAAGGAGATTTCAGAAAAATATTCACCGTTGTTTTAAACCCTTTTGTGTCTCTGTTGTTTTTCTCTGTTCTTTTCTCCCCTTTTCCTTTTTTCTTTCGTTTCCTCTTTTTTTTTTTTATCAGTGTAC,ATATACGTTGTGAAGGAATGACCCTCGGGAACGCTGAA
M05522:218:000000000-C5JTY:1:2104:27057:18742 2:N:0:1	M05522:218:000000000-C5JTY:1:2104:27057:18742 1:N:0:1	-1	1620415	GCAAAGCTCCCTGTACCTTACGGCCTCCCAGCTCAGTTACTCAGGAACCTACTTCTGCGGCACAGAGACACAGTGATACCCAGGCCTCCAAGACCTGTACTCAAACCTAAAGCTGAGCCGCAGATGCTCCCCTAGCACAGATGCCCACCACAGGAGTATGGGGAACTTACCAGAAGGTTCATCCATGATAAAAGAGAAACCTGAAGGAAATTCATTTGCTTCAACACATAAAACAAAAAGACTCAGGG,AAAAAAAGCCTTACGGCCTTATTCTCGGGAAC
M05522:218:000000000-C5JTY:1:1101:12414:2283 2:N:0:1	M05522:218:000000000-C5JTY:1:1101:12414:2283 1:N:0:1	-1	290	CTGCACATCACAGCCCCCACCCCTGCCGACTCAGCCCCCTCTCTCTGCGCTGTGCAACCTTCGGGAGGAGGCAACAAACTCACCTTTGGGACAGGCACTCCGCTACAGTGGCACTCAATATCCAGTACCCTGACCCTGCCGTGTACCTGCTGTTTGTCTCTTTTTCCTGTGTCTTTTCTGTCTTCCTTTTCTCTCTTTTTTTTTTTTTTTTTTTTTTTTCTTTTTTTTTTTTTTTTTTAATTATATCA,AAAAAAAGGCACGACCAAGTGCTCTCGGGAACGCTGAA
M05522:218:000000000-C5JTY:1:2104:3657:19263 2:N:0:1	M05522:218:000000000-C5JTY:1:2104:3657:19263 1:N:0:1	-1	1622563	GCAAAGCTCCCTGTACCTTACGGCCTCCCCGCTCAGTTACTCAGGAACCTACTTCTGCGGCACAGAGACACAGTGATACCCAGGCCTCCAAGACCTGTACTCAAACCTAAAGCTGAGCCGCGGATGATCCCCTAGCACAGATGCCCACCACAGGAGTATGGGGAACTTACCAGAAGGTTCATCCATGATAAAAGAGAAACCTGAAGGAAATTCATTTGCTTCAACACATAACACAAAAAGATGACAAG,AAAAAAAACCTCACCGTGACTGTCTCGGGAACGC
M05522:218:000000000-C5JTY:1:1101:18362:2368 2:N:0:1	M05522:218:000000000-C5JTY:1:1101:18362:2368 1:N:0:1	-1	424	TCCACCTTGGAGATCCAGCGCACACAGCAGGAGGACTCGGCCGTGTATCTCTGTGCCAGCAGCTTAGTTCACGGGAGCTCCTACAATGAGCAGTTCTTCGGGCCAGGGACACGGCTCACCGTGCTAGAGGACCTGAAAAACGTGTTCCCACCCGTGGTCGCTGTGTTTGTGCCTTCTGTTTCTTTTTTCTCCCTTTCCCTTTTTTCCTTTCTTTTTTTCCTTTCCTCCCTCCTCTTCCCCCGGTTTAG,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```
line count: 52,341

### `*paired_clones.txt` (14 files)

inspected: `SCP1348/SCP1348/other/V39_paired_clones.txt` (31.01 KB)

delimiter: tab; columns in first line: 28
first lines:
```text
cloneId	cloneCount	cloneFraction	targetSequences	targetQualities	allVHitsWithScore	allDHitsWithScore	allJHitsWithScore	allCHitsWithScore	allVAlignments	allDAlignments	allJAlignments	allCAlignments	nSeqImputedFR1	minQualFR1	nSeqImputedCDR1	minQualCDR1	nSeqImputedFR2	minQualFR2	nSeqImputedCDR2	minQualCDR2	nSeqImputedFR3	minQualFR3	nSeqImputedCDR3	minQualCDR3	nSeqImputedFR4	minQualFR4	aaSeqImputedFR1
0	194.0	0.15168100078186084	TCCTCTTCCCAGACCACAGACTCAGGCGTTTATTTCTGTGCTGGTATTTCTAATGCAGGCAACATGCTCACCTTTGGAGGGGGAACAAGGTTAATGGTCAAACCCCGTGAGTATCTCTGCTGAATCCATAATGAATGCTCTAATTTCAAAAGGAAGCCGTAGCACTGAGCTCTGTTTTCTGTTTT,ATTTTTTCTTTTTTTTTTATTTT	4/1,/2036:[015/31[:[403;6/1[1[:;[574((((((((((((((((((((((((((((((((((((((([:,2[2[[(-21/[[0[./9[[123//4:;6[0[)[.-5570[;14[%)3/3+40/[3'+66+40[*,:6[/),,,29*/3+57.(6
1	132.0	0.10320562939796717	TGCAGCTACTCAACCTGGAGACTCAGCTGTCTACTTTTGTGCAGTTGGAGTGTACAATGCCAGACTCATGTTTGGAGATGGAACTCAGCTGGTGGTGAAGCCCAGTAAGTGGACATGTTTTATTGATATTTGACCAAACAAATAAATCCCGTGAAGTT,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	[42[8,4-[-[[,4[[689[[99[[[[5[9[[856[[************************************[9,[-[[[)28[51[5[[[*[[+[-/7-82-6/4-8,9['0,18/[
2	132.0	0.10320562939796717	CCGTGCAGCCTGAAGATTCAGCAACTTACTTTTGTCAACAGGCTAACAGTTTCCCCACTTTCGGCCCTGGGACCAAAGTGGAAATCCAACGAACTGTGGCTGCACCCTCTGTCTTC	55835[[4[8[9.0[/[998834[[69344[6''''''''''''''''''''''''''''''8[[5[9[8['[[)('8/[[$()[1[(*[[&)243/[[0.[[$4[$214//31[0	IGKV1D-12*00(213.6),IGKV1-12*00(211.5)		IGKJ3*00(114.7)	IGKC*00(292.3)	232|284|307|3|55|ST247CST248ASA259T|218.0;261|284|305|32|55||115.0	
3	106.0	0.08287724784988272	ATCCAGCCCTCAGAACCCAGGGACTCAGCTGTGTACTTCTGTGCCATACTTACCGGGGAGCTGTTTTTTGGAGAAGGCTCTAGGCTGACCGTACTGG,CGTGTTCCCCCCCGCGGTCGCTGTGTTT	[[7[1888[[[75/-[[8/[[[.[8[1[5[35[8+[4[[##############################[4&7%,[[[[[2&7[828%28[2%[[7[,17+758-4[$[7[)%/7*0.[)2.1,7[	TRBV12-3*00(216.7),TRBV12-4*00(216.7)		TRBJ2-2*00(201.7)	TRBC2*00(150.3)	234|280|310|0|46||230.0,;273|280|310|39|46||3
4	74.0	0.05785770132916341	AGCAGTGCCCATCCTGAAGACAGCAGCTTCTACATCTGCAGTGCTACCTGGGACAGCGAGCAGTACTTCGGGCCGGGCACCAGGCTCACGGTCACAGAGGACCTGAAAAACGTGTTCCCACCCG,CCCCCCCAAGGCCCCCCTGG	[[[[100002/0[[7[//62[5[[1[[[[[[6[2[[&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&[[[[[[[[[*[['[[[0[)[[66[%[%[&[[%[[6[$**,*[[-[61[[[%[[[/,3&6[['$%$,5[6&[&3&..	TRBV20-1*00(216.3)	TRBD1*00(36)	TRBJ2-7*00(187.9)	TRBC2*00(298.8)	245|289|313|2|4
```
line count: 35

### `*slide_seq.pdf` (1 file)

inspected: `SCP1348/SCP1348/other/Supplementary Figure 5B_slide_seq.pdf` (383.49 KB)

binary: PDF

### `*submit.h5ad` (2 files)

inspected: `SCP1348/SCP1348/anndata/2021-09-01_Puck_210731_12_submit.h5ad` (2.22 GB)

AnnData (.h5ad) summary:
X: dense, shape=(21313, 5252), dtype=float32
obs: 21313 rows, 6 columns; index '_index' (first ids: ['TCTCTACTTGTCTA-1', 'AAAACAAAAAAAAA-1', 'TTTACACGCTTTCT-1'])
| column | dtype | first values |
|---|---|---|
| n_genes | int64 | [3716, 2297, 1602] |
| n_genes_by_counts | int64 | [3700, 2162, 1597] |
| total_counts | float32 | [7730.0, 2646.0, 2776.0] |
| total_counts_mt | float32 | [93.0, 2.0, 37.0] |
| pct_counts_mt | float32 | [1.2031047344207764, 0.07558578997850418, 1.3328529596328... |
| leiden | categorical (21 levels: 0, 1, 2, 3, 4, 5, 6, 7) | 6, 2, 6 |
var: 5252 rows, 12 columns; index '_index' (first ids: ['A2ML1-AS1', 'AADACL2-AS1', 'AADAT'])
| column | dtype | first values |
|---|---|---|
| n_cells | int64 | [14, 11, 5] |
| mt | bool | [False, False, False] |
| n_cells_by_counts | int64 | [14, 11, 5] |
| mean_counts | float32 | [0.000647938170004636, 0.0005553755909204483, 0.000231406... |
| pct_dropout_by_counts | float64 | [99.93520618318138, 99.94909057249966, 99.9768593511362] |
| total_counts | float32 | [14.0, 12.0, 5.0] |
| highly_variable | bool | [True, True, True] |
| means | float64 | [0.0469582509214151, 0.032173776443552085, 0.012618013264... |
| dispersions | float64 | [4.765000284876938, 4.549856057410516, 4.684879387907584] |
| dispersions_norm | float32 | [1.176964521408081, 0.574292004108429, 0.9525259733200073] |
| mean | float64 | [4.507113161239397e-11, -2.195794086915394e-12, -3.397899... |
| std | float64 | [0.10380160871328843, 0.09047632151665708, 0.055955315919... |
obsm: X_pca (21313, 50); X_umap (21313, 2)
varm: PCs (5252, 50)
obsp: connectivities (group); distances (group)
uns keys (7): hvg, leiden, leiden_colors, neighbors, pca, rank_genes_groups, umap
HDF5 tree (depth <= 3):
```text
X  dataset shape=(21313, 5252) dtype=float32
obs/ [dataframe]
  __categories/
    leiden  dataset shape=(21,) dtype=object
  _index  dataset shape=(21313,) dtype=object
  leiden  dataset shape=(21313,) dtype=int8
  n_genes  dataset shape=(21313,) dtype=int64
  n_genes_by_counts  dataset shape=(21313,) dtype=int64
  pct_counts_mt  dataset shape=(21313,) dtype=float32
  total_counts  dataset shape=(21313,) dtype=float32
  total_counts_mt  dataset shape=(21313,) dtype=float32
obsm/
  X_pca  dataset shape=(21313, 50) dtype=float32
  X_umap  dataset shape=(21313, 2) dtype=float32
obsp/
  connectivities/ [csr_matrix]
    data  dataset shape=(372526,) dtype=float32
    indices  dataset shape=(372526,) dtype=int32
    indptr  dataset shape=(21314,) dtype=int32
  distances/ [csr_matrix]
    data  dataset shape=(191817,) dtype=float64
    indices  dataset shape=(191817,) dtype=int32
    indptr  dataset shape=(21314,) dtype=int32
raw/ [raw]
  X  dataset shape=(21313, 20295) dtype=float32
  var/ [dataframe]
    _index  dataset shape=(20295,) dtype=object
    dispersions  dataset shape=(20295,) dtype=float64
    dispersions_norm  dataset shape=(20295,) dtype=float32
    highly_variable  dataset shape=(20295,) dtype=bool
    mean_counts  dataset shape=(20295,) dtype=float32
    means  dataset shape=(20295,) dtype=float64
    mt  dataset shape=(20295,) dtype=bool
    n_cells  dataset shape=(20295,) dtype=int64
    n_cells_by_counts  dataset shape=(20295,) dtype=int64
    pct_dropout_by_counts  dataset shape=(20295,) dtype=float64
    total_counts  dataset shape=(20295,) dtype=float32
uns/
  hvg/
    flavor  dataset shape=() dtype=object
  leiden/
    params/
  leiden_colors  dataset shape=(21,) dtype=object
  neighbors/
    connectivities_key  dataset shape=() dtype=object
    distances_key  dataset shape=() dtype=object
    params/
  pca/
    params/
    variance  dataset shape=(50,) dtype=float32
    variance_ratio  dataset shape=(50,) dtype=float32
  rank_genes_groups/
    logfoldchanges  dataset shape=(20295,) dtype=[('0', '<f4'), ('1', '<f4'), ('2', '<f4'), ('3', '<f4'), ('4', '<f4'), ('5', '<f4'), ('6', '<f4'), ('7', '<f4'), ('8', '<f4'), ('9', '<f4'), ('10', '<f4'), ('11', '<f4'), ('12', '<f4'), ('13', '<f4'), ('14', '<f4'), ('15', '<f4'), ('16', '<f4'), ('17', '<f4'), ('18', '<f4'), ('19', '<f4'), ('20', '<f4')]
    names  dataset shape=(20295,) dtype=[('0', 'O'), ('1', 'O'), ('2', 'O'), ('3', 'O'), ('4', 'O'), ('5', 'O'), ('6', 'O'), ('7', 'O'), ('8', 'O'), ('9', 'O'), ('10', 'O'), ('11', 'O'), ('12', 'O'), ('13', 'O'), ('14', 'O'), ('15', 'O'), ('16', 'O'), ('17', 'O'), ('18', 'O'), ('19', 'O'), ('20', 'O')]
    params/
    pvals  dataset shape=(20295,) dtype=[('0', '<f8'), ('1', '<f8'), ('2', '<f8'), ('3', '<f8'), ('4', '<f8'), ('5', '<f8'), ('6', '<f8'), ('7', '<f8'), ('8', '<f8'), ('9', '<f8'), ('10', '<f8'), ('11', '<f8'), ('12', '<f8'), ('13', '<f8'), ('14', '<f8'), ('15', '<f8'), ('16', '<f8'), ('17', '<f8'), ('18', '<f8'), ('19', '<f8'), ('20', '<f8')]
    pvals_adj  dataset shape=(20295,) dtype=[('0', '<f8'), ('1', '<f8'), ('2', '<f8'), ('3', '<f8'), ('4', '<f8'), ('5', '<f8'), ('6', '<f8'), ('7', '<f8'), ('8', '<f8'), ('9', '<f8'), ('10', '<f8'), ('11', '<f8'), ('12', '<f8'), ('13', '<f8'), ('14', '<f8'), ('15', '<f8'), ('16', '<f8'), ('17', '<f8'), ('18', '<f8'), ('19', '<f8'), ('20', '<f8')]
    scores  dataset shape=(20295,) dtype=[('0', '<f4'), ('1', '<f4'), ('2', '<f4'), ('3', '<f4'), ('4', '<f4'), ('5', '<f4'), ('6', '<f4'), ('7', '<f4'), ('8', '<f4'), ('9', '<f4'), ('10', '<f4'), ('11', '<f4'), ('12', '<f4'), ('13', '<f4'), ('14', '<f4'), ('15', '<f4'), ('16', '<f4'), ('17', '<f4'), ('18', '<f4'), ('19', '<f4'), ('20', '<f4')]
  umap/
    params/
var/ [dataframe]
  _index  dataset shape=(5252,) dtype=object
  dispersions  dataset shape=(5252,) dtype=float64
  dispersions_norm  dataset shape=(5252,) dtype=float32
  highly_variable  dataset shape=(5252,) dtype=bool
  mean  dataset shape=(5252,) dtype=float64
  mean_counts  dataset shape=(5252,) dtype=float32
  means  dataset shape=(5252,) dtype=float64
  mt  dataset shape=(5252,) dtype=bool
  n_cells  dataset shape=(5252,) dtype=int64
  n_cells_by_counts  dataset shape=(5252,) dtype=int64
  pct_dropout_by_counts  dataset shape=(5252,) dtype=float64
  std  dataset shape=(5252,) dtype=float64
  total_counts  dataset shape=(5252,) dtype=float32
varm/
  PCs  dataset shape=(5252, 50) dtype=float64
```

### `*tcr_labels_filt_tumor.csv` (8 files)

inspected: `SCP1348/SCP1348/Fastq/mel08_tcr_labels_filt_tumor.csv` (12.03 KB)

delimiter: comma; columns in first line: 22
first lines:
```text
"TCATCCACACGCGC-1","TTAGNATCCTTGAG-1","TACGAAGCCGCTAA-1","CATGAACTACACGA-1","CGCCGCAGAACACT-1","CTCCCTTCTAACTG-1","CATATACAGAGGTG-1","TGCCGCGCACCAGT-1","CTAAGCCACATTTA-1","ATCCGTCAGTGTAG-1","CAGCACTCCAGGTT-1","AGGGATTTGTTACG-1","ACTCTTCCTGTAGG-1","CAAAGAGGGGACAA-1","ATGGATCTTATCTA-1","GGTTGCCGACAGCT-1","CTCACAGGCCTTAT-1","CTCTTAATGCATTG-1","ACATCCCCCGGCAG-1","CACACGTCCAACCG-1","TTGCTCATTAGTGG-1","
"0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",

```
line count: 2

### `*tcr_labels_filt_tumor_exclusive.csv` (7 files)

inspected: `SCP1348/SCP1348/Fastq/mel08_tcr_labels_filt_tumor_exclusive.csv` (57.69 KB)

delimiter: comma; columns in first line: 24
first lines:
```text
"CCGGGAGGCCCTCG","GAGAGGTTAGGGTT","AATTCAGCCTTTAG","TCGNAGTGCAAGCC","TTTGCAATAAGACT","AGTTGAATTNCTAG","GGTGACTCTGACGT","GACGGATGCTGGCA","GACTTACCGGGCCT","TCCGCCGAGCCTAT","CTCGTGCGAGATTA","AGTGCCAGCATATC","TGTCGAACCACCTA","CCCAACCTGTTGGC","ATATTTTTTATGGC","CGTGGAGAAGGCCT","TTTCAAACGCGTTA","ACACCGTTTACCTG","AGACACGGCTAAAG","GAACTGCCNTAAGA","TGTGTAGGGCGGAA","ATTCTTAATTATCC","CCGATGTTGGGACT","CTAAATGT
"0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",

```
line count: 2

### `Aggregated_clusterassignments.csv` (1 file)

inspected: `SCP1348/SCP1348/other/Aggregated_clusterassignments.csv` (3.11 MB)

delimiter: comma; columns in first line: 2
first lines:
```text
"barcode","cluster"
"rep8_TCCTCGCGGCAGGA","6"
"rep8_AAAAAAAAAAAACA","9"
"rep8_AGGTCCGGCCGCTC","0"
"rep8_AGCACAATCCATGG","2"
"rep8_CTCCAGGCTAGTTC","0"
```
line count: 117,741

### `Aggregated_clusterassignments_pretreatment.csv` (1 file)

inspected: `SCP1348/SCP1348/other/Aggregated_clusterassignments_pretreatment.csv` (2.06 MB)

delimiter: comma; columns in first line: 2
first lines:
```text
"barcode","cluster"
"rep12_GGTGAGAAGCATTG","4"
"rep12_ACAAACAGTCACGA","0"
"rep12_CGCTAACCGCGGTT","0"
"rep12_TCGTATGCTACCCA","4"
"rep12_CCCGCGAATGCCAC","3"
```
line count: 75,929

### `ERV_loc_counts.csv` (1 file)

inspected: `SCP1348/SCP1348/other/ERV_loc_counts.csv` (874.94 KB)

delimiter: comma; columns in first line: 7
first lines:
```text
,tumor_beads,n_genes_by_counts,total_counts,n_counts,x,y
TCCTCGCGGCAGGA,0,20,23.0,23.0,3283.6,2346.0
AGGTCCGGCCGCTC,1,9,11.0,11.0,2581.9,5379.9
AGCACAATCCATGG,0,12,15.0,15.0,3045.6,1373.4
CTCCAGGCTAGTTC,1,20,28.0,28.0,1971.4,3674.2
AATCCACCCCTCGA,1,24,36.0,36.0,3600.2,5141.4
```
line count: 21,285

### `HARLEQUIN*locs.csv` (3 files)

inspected: `SCP1348/SCP1348/other/HARLEQUIN_1q24.3_locs.csv` (39.09 KB)

delimiter: comma; columns in first line: 3
first lines:
```text
,x,y
0,3283.6,2346.0
1,2389.7,1795.1
2,1971.4,3674.2
3,1840.7,4466.8
4,1413.7,4779.4
```
line count: 2,117

### `Merged_mouse*.fastq.gz` (1 file)

inspected: `SCP1348/SCP1348/fastq/Merged_mouse_spleen2_L001_R1_001.fastq.gz` (782.61 MB)

first two reads:
```text
@M00136:340:000000000-CYW3P:1:1101:16426:1395 1:N:0:1
TCCCTTGGTCTTCAGCGTTCCCGAGAGTTGCGTGACAAGCATTTTTTT
+
ABAAABFBDFDFFGFGGGGFGGGEC22FEGGEEGEG5FGGCGGHFHCE
@M00136:340:000000000-CYW3P:1:1101:14718:1398 1:N:0:1
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
+
BBBBBBDDBBBBGGGGGGGGGGGGGGGGGGGGGGGGGGGCGGGGGGGG
```

### `Merged_mouse_spleen_paired_cloneID.txt` (1 file)

inspected: `SCP1348/SCP1348/other/Merged_mouse_spleen_paired_cloneID.txt` (695.11 MB)

delimiter: tab; columns in first line: 8
first lines:
```text
descrsR2	descrsR1	cloneId	readId	targetSequences	topChains	chains	cloneMapping
M00136:340:000000000-CYW3P:1:1106:20784:26360 2:N:0:1	M00136:340:000000000-CYW3P:1:1106:20784:26360 1:N:0:1	-1	2477618	AGACTCTCAGCCTGGAGCCTCAGCTACCTTCTTCTGCGCAGCCAGCGCCCACTCTCCGTCGATCTGGGGCTCGGGGCCCAAGCTGATTTTAAAGCCAGACATCCAGAACCCAGACCCTGCTGTGTGCCGGGTAAAGGCTCCCCCGTCTCGGGACAGCACCCGCGGCCTGTTCCCCGCCTTTGGCTCCCAAATCAATGTGCCGACAACCCTGGGATCTGGAACGGTCATCCCTGTCAAACCGGTGCTGG,AAAAAAAAAAAAAAAAAAAATCAGAGTACAGC
M00336:791:000000000-J22PY:1:2114:16209:29132 2:N:0:1	M00336:791:000000000-J22PY:1:2114:16209:29132 1:N:0:1	-1	21271768	GCTTCGAGGCTGAGTTCAGCTTTCCCGAGACTCTTTTCTGCCTTTTTTTTTTTTTTTTTTTTTTTTCTTTTTTTTTCTTTCTTTTTTTCTTTTTTTTTTCTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTCTCTTTT	TRA	TRA	-1:dropped
M00136:340:000000000-CYW3P:1:1106:17009:26364 2:N:0:1	M00136:340:000000000-CYW3P:1:1106:17009:26364 1:N:0:1	-1	2477646	AGACTCTCAGGCTGGGGACTCCGCTGCCTATTTCTGTGCAGCAAGGGACCGCTATCAGTTGGTCTGGGGCTCTGGGACCAAGCTAATTATAAAGCCAGCCATCCAGAACCCAGAACCTGCTGGGTCCCCGTTAAAAGATCCTCGGGCTCCGGACAGCACCCTCTGCCTGTTCACCGACTTTGACTCCCAAATCAATGTGCCGGAAACCATGGGATCTGGAAGGTTCATCACTGACAAAACTGTGCTGG,AAAAAAAAAAAAAAAAAACGAGCCTCCCGGAC
M00336:791:000000000-J22PY:1:2114:15716:29220 2:N:0:1	M00336:791:000000000-J22PY:1:2114:15716:29220 1:N:0:1	-1	21271826	ACCAGCAGATTCTCAGTCCAGCAGTTTGCTGACTCTCACCCTGACATGGCCCTGAGAGCCTTGGCACCGGAGGACTCCGCTACGTACTTCCGTGCCAGCTCTCGGGCCAATTATGCACAGTACCTCGGTCCCGGCCCCCGGCCCACGGCTTTAGAGGATCTGAGACATGTGACCCCCCCCAAGGCCCCCTCGTTCGCGCCCTCACCCGCAGAGTTTGCCACCCAACAACCGGCCCCCCCCGTGTGCTT,AAAAAAAGCGGAGGAGCCCGGGTCTCGGGAA
M00136:340:000000000-CYW3P:1:1106:18386:26365 2:N:0:1	M00136:340:000000000-CYW3P:1:1106:18386:26365 1:N:0:1	-1	2477658	CTCAGCAGATTCTCAGACAAACCGTTTGATCACTCTCACTCTGAAATGAACACGAGCGCCTTGGACATGGAGGACGCTGCTACGTACTTCAGCGCCAGCCCGCGGGCCAATTCCGAACAGTCCTTAGGTCCCGGCACCAGGCTCACGGGTTTAGAGGCACTGAGAAATGTGCCCCCACCCAAGGTCCCCCTGTTTGAGCCATCAAAAGCAGAGATTGCAAACAAACAAAAGGCCACCCTCGTGTTCCT,AAAAAAAGGCGGGTTCAACGGCTCTCGGGAAC
```

### `Merged_mouse_spleen_paired_clones.txt` (1 file)

inspected: `SCP1348/SCP1348/other/Merged_mouse_spleen_paired_clones.txt` (89.82 KB)

delimiter: tab; columns in first line: 28
first lines:
```text
cloneId	cloneCount	cloneFraction	targetSequences	targetQualities	allVHitsWithScore	allDHitsWithScore	allJHitsWithScore	allCHitsWithScore	allVAlignments	allDAlignments	allJAlignments	allCAlignments	nSeqImputedFR1	minQualFR1	nSeqImputedCDR1	minQualCDR1	nSeqImputedFR2	minQualFR2	nSeqImputedCDR2	minQualCDR2	nSeqImputedFR3	minQualFR3	nSeqImputedCDR3	minQualCDR3	nSeqImputedFR4	minQualFR4	aaSeqImputedFR1
0	222076.0	0.35802194471582466	CCCAGCAGATTCTCAGTCCAACAGTTTGATGACTATCACTCTGAAATGAACATGAGTGCCTTGGAACTGGAGGACTCTGCTATGTACTTCTGTGCCAGCTCTCGGGCCAATTATGAACAGTACTTCGGTCCCGGCACCAGGCTCACGGTTTTAGAGGATCTGAG	3/1353/405032312113//1/70335-.3.45035044456,,./8.06/17-4*958./97.070:;.:;.7161:61,16-/6356%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%;;07997:7*89,977-7)365,344,6',,**+0+&+	TRBV12-1*00(483.7)		TRBJ2-7*00(204.7)	T
1	120248.0	0.19385896183373477	AGGAAGATGGACGATTCACAATCTTCTTCAATAAAAGGGAGAAAAAGCTCTCCTTGCACATCACAGACTCTCAGCCTGGAGACTCAGCTACCTACTTCTGTGCAGCAAGTGACAACTATCAGTTGATCTGGGGCTCTGGGACCAAGCTAATTATAAAGCCAGACATCCAGAACCCAGAACCTGCTGTGTACCAGTTAAAAGATCCTCGGTCTCAGGACAGCACCCTCTGCCTGTTCACCGACTTTG	-101/1-012041./,.062/1217/2021/5///-/11.3/210021-3-53-.420300'13/3*2*3-43413214+2/1541505133606555%%%%%%%%%%%%%%%%%%%%%%%%
2	24098.0	0.03884982088907375	CCCAGCAGATTCTCAGTCCAACAGTTTGATGACTATCACTCTGAAATGAACATGAGTGCCTTGGAACTGGAGGACTCTGCTATGTACTTCTGTGCCAGCTCTCGGGCCCATTATGAACAGTACTTCGGTCCCGGCACCAGGCTCACGGTTTTAGAGGATCTGAG,CCCAAGGTCTCCTTGTTTGAGCC	3/1144,4.40524.4225,,3,82457*/4+67-48-66776))+/8,-8,27*2*:7:./96,-:09;+9;+9181881)07-,9459$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$:;/8:;8;9(:;)97:+:'386+565*8&--'*-0-%-,503''--),,321,/,
3	17878.0	0.02882218847434893	CCCAGCAGATTCTCAGTCCAACAGTTTGATGACTATCACTCTGAAATGAACATGAGTGCCTTGGAACTGGAGGACTCTGCTATGTACTTCTGTGCCAGCTCTCGGGCCAATTATGACCAGTACTTCGGTCCCGGCACCAGGCTCACGGTTTTAGAGGATCTGAGAAATG,CCCAAGGTCTCCTTGTTTGAGCCAT	4/1144,3.50534/4224-,2-92446+/4+57-47-65677**+/8,-8,27*3*:7;./96,-80::+:;+9181981)09-,7358$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$::/::;9;:(:;):6:+:'386,566*7&..(+.0.%-(,),-,603'
4	17289.0	0.027872626498099264	CCCAGCAGATTCTCAGTCCAACAGTTTGATGACTATCACTCTGAAATGAACATGAGTGCCTTGGAACTGGAGGACTCTGCTATGTACTTCTGGGCCAGCTCTCGGGCCAATTATGAACAGTACTTCGGTCCCGGCACCAGGCTCACGGTTTTAGAGGATCTGAG,CCCAAGGTCTCCTTGTTTGAGCC	2-/231-2.3-20106//1-./.6/234+-3,34.24-34446**,,8,-5-.6+2':58+-86,-7-9;+:<+6.4.95.*.8*,6025####################################:=,7:99<7)88+:78*8)176*354+6'--(*,.,&,,3.1((,,(,+11/+/
```
line count: 84

### `Puck*NanoporeTCR_BC_UMI_reads.csv` (1 file)

inspected: `SCP1348/SCP1348/other/Puck_211105_07_NanoporeTCR_BC_UMI_reads.csv` (2.98 MB)

delimiter: comma; columns in first line: 7
first lines:
```text
,bc,umi,cloneMapping,cloneId,topChains,chains
61e7b9ad-6ff4-402b-90d3-3e6b5dc4ba20,CTGGCCTCACTTCC,ATTTGATCT,1:core,1,TRA,TRA
f8ab63cc-8b9b-495f-90ab-f2c90edbab3f,CTGGCCTCACTTCC,ATTTGATCT,1:core,1,TRA,TRA
4fd3192a-3832-4287-8251-a8d84e6aa161,CTGGCCTCACTTCC,GCAAATTAA,1:core,1,TRA,TRA
f4d36772-08ea-46db-89cf-6cbb2b56feb0,CTGGCCTCACTTCC,ATTTGATCT,3:core,3,TRA,TRA
3102c251-fb10-468c-b1fd-11856d653b78,CTGGCCTCACTTCC,ATTTGATCT,1:core,1,TRA,TRA
```
line count: 37,449

### `Puck*barcode_matching.txt` (11 files)

inspected: `SCP1348/SCP1348/other/Puck_220408_15_barcode_matching.txt` (1.24 MB)

delimiter: tab; columns in first line: 6
first lines:
```text
IlluminaBarcodes	ProcessedIlluminaBarcodes	BeadBarcodes	Distance	X	Y
CGAGAACGAAGGGT	CGAGAACGAAGGGT	CGAGNACRAAGGGT	0	1540.23	2510.97
CTCCCCCGGCTCTT	CTCCCCCGGCTCTT	CTCCCCCGGCTCTT	0	2839.9	2616.5
GTCGGAACGATGGT	GTCGGAACGATGGT	GTCGGAACGATGGT	0	3575	872.59
ACCTATAGCATTGT	ACCTATAGCATTGT	ACCTATAGCATTGT	0	929.35	2857.4
CCGTAGACATTTCT	CCGTAGACATTTCT	CCGTAGACATTTCT	0	2007.8	1252.7
```
line count: 20,478

### `Puck*cell_clones.csv` (11 files)

inspected: `SCP1348/SCP1348/other/Puck_220408_08_cell_clones.csv` (4.85 MB)

delimiter: comma; columns in first line: 18
first lines:
```text
,x,y,B-cell,CD4,Tfh,Treg,CD8 Exh.,CD8 NonExh.,Myeloid,Plasma,Tumor,type,maxw,TRBs,CloneSize,LogCloneSize,spot
ATGCTGGCAGCATG-1,2883.5,2444.7,0.3008767530322075,0.40238353312015535,0.49958744943141936,0.5994395732879638,0.8353457421064376,0.5026322662830353,0.4682645916938782,0.05472727380692959,1.5190285205841065,Tumor,0.2931194086044484,,,,Lobe2
CCTTCCTCCTCGCC-1,2110.7,3427.9,0.4592522069811821,0.4610229730606079,0.43421068489551545,0.5832617491483688,0.5493172526359559,0.8576913714408875,0.588593503832817,0.7378874719142914,0.1562219478189945,CD8 NonExh.,0.1776693168614532,,,,Fibrostromal
CCCAAGCCCTACTC-1,2394.3,3257.5,0.956719183921814,0.4410264685750008,0.4837564989924431,0.5546136617660523,0.73223477602005,0.7159522116184235,0.24071353375911714,0.8830285042524337,0.1865287244319916,B-cell,0.18417665516842857,,,,Fibrostromal
ACCCAACTAGTTAC-1,2158.9,2387.2,0.18117956668138505,0.12584521099925042,0.10589448846876622,0.08968401774764061,0.08805125355720521,0.26575313210487367,0.6851977944374085,0.9670561760663986,0.15730247646570206,Plasma,0.36274163259391834,,,,Fibrostromal
ACAGCTCTACATGT-1,2818.7,2503.8,0.2450905993580818,0.21604404225945473,0.2274886228144169,0.2273180589079857,0.17411011978983879,0.5078976333141327,0.7453713178634643,0.016053584311157467,1.4392669439315795,Tumor,0.378889969669828,,,,Lobe2
```
line count: 19,035

### `Puck*clone_bcumi.csv` (5 files)

inspected: `SCP1348/SCP1348/other/Puck_220408_14_clone_bcumi.csv` (1.45 MB)

delimiter: comma; columns in first line: 4
first lines:
```text
chains,cloneId,bc,umi
TRA,0,AAAAAATGAAGATG,ATACCCATG
TRA,0,AAAAACTCACTGCA,GTGAGTTCA
TRA,0,AAAAAGGTAGCTAA,CACAGGCCA
TRA,0,AAAACAGCAACGGA,ACTGCCATT
TRA,0,AAAAGAATATTAAC,TCTCATAGA
```
line count: 44,943

### `Puck*clones.txt` (5 files)

inspected: `SCP1348/SCP1348/other/Puck_220420_17_clones.txt` (123.77 KB)

delimiter: tab; columns in first line: 28
first lines:
```text
cloneId	cloneCount	cloneFraction	targetSequences	targetQualities	allVHitsWithScore	allDHitsWithScore	allJHitsWithScore	allCHitsWithScore	allVAlignments	allDAlignments	allJAlignments	allCAlignments	nSeqImputedFR1	minQualFR1	nSeqImputedCDR1	minQualCDR1	nSeqImputedFR2	minQualFR2	nSeqImputedCDR2	minQualCDR2	nSeqImputedFR3	minQualFR3	nSeqImputedCDR3	minQualCDR3	nSeqImputedFR4	minQualFR4	aaSeqImputedFR1
0	2343261.0	0.7047556232061636	TGTGCCAGCTCTCGGGCCAATTATGAACAGTACTTC	{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{	TRBV12-1*00(479.9)		TRBJ2-7*00(210.3)	TRBC2*00(238.2),TRBC1*00(230)	270|283|305|0|13||65.0		24|39|67|21|36||75.0	;	gattctggggttgtccagtctccaagacacataatcaaagaaaagggaggaaggtccgttctgacgtgtattcccatc		tctggacatagcaat		gtggtctggtaccagcagactctggggaaggaattaaagttccttattcag		cattatgaaaaggtggag		agagacaaag
1	973322.0	0.2927348480132045	TGTGCAGCAAGTGACAACTATCAGTTGATCTGG	{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{	TRAV14N-2*00(309.2),TRAV14N-1*00(308.6),TRAV14D-2*00(307.9),TRAV14D-1*00(307.8)		TRAJ33*00(244.6)	TRAC*00(239.6)	267|280|300|0|13||65.0;267|280|300|0|13||65.0;267|280|300|0|13||65.0;267|280|300|0|13||65.0		27|46|77|14|33||95.0		cagcagcaggtgagacaaagtccccaatctctgacagtctgggaaggagagacagcaattctgaactgcagtta
2	868.0	2.6105836308586627E-4	TGTGCCAGCTCTCGGGCCAATTATGACAGGTCTCC	QRNTNM{UQ{{{{{ScQU{{PGC?ACGICIKHHIK	TRBV12-1*00(470.7)		TRBJ2-7*00(141.6)	TRBC2*00(228.8),TRBC1*00(221.2)	270|283|305|0|13||65.0		24|39|67|21|35|DA29ST33GSA34TST37C|16.0	;	gattctggggttgtccagtctccaagacacataatcaaagaaaagggaggaaggtccgttctgacgtgtattcccatc		tctggacatagcaat		gtggtctggtaccagcagactctggggaaggaattaaagttccttattcag		cattatgaaaag
3	593.0	1.7834978031096622E-4	TGTGCAGCAAGTGACCATCAGTTGATCTGG	MRPML{PJIGHGEFFFLPKOMSVMdPOKM{	TRAV14N-2*00(277.8),TRAV14N-1*00(274.9),TRAV14D-2*00(274.1),TRAV14D-1*00(273.5)		TRAJ33*00(208.8)	TRAC*00(215.8)	267|280|300|0|13||65.0;267|280|300|0|13||65.0;267|280|300|0|13||65.0;267|280|300|0|13||65.0		29|46|77|13|30|ST31C|71.0		cagcagcaggtgagacaaagtccccaatctctgacagtctgggaaggagagacagcaattctgaactgcagttat
4	530.0	1.5940199589344368E-4	TGTGCCAGCAGTGAACTGGGGGGAAGTCAAAACACCTTGTACTTT	{{{{{]{P_SQ{OPTO{OVSO{R{{PWN{R{{{{{{UNNP{{{{Q	TRBV13-3*00(427.1)	TRBD2*00(45)	TRBJ2-4*00(234.1)	TRBC2*00(234.3),TRBC1*00(226.6)	270|284|306|0|14||70.0	17|26|42|14|23||45.0	20|41|69|24|45||105.0	;	gaggctgcagtcacccaaagtccaagaagcaaggtggcagtaacaggaggaaaggtgacattgagctgtcaccagact		aataaccatgactat		atgtactggtatcggcaggacacggggcatg
```
line count: 158

### `Puck*expression.txt` (7 files)

inspected: `SCP1348/SCP1348/other/Puck_200727_02.digital_expression.txt` (1.72 GB)

delimiter: tab; columns in first line: 28
first lines:
```text
GENE	TTTTTTTTTTTTTT	AAAAGAAAAAAAAA	AGATTTTAGAGCGA	CCCGTAATTGGGCT	AACCGGTCAGGCTT	AAGCCGTGACCCGT	CCACTGGGGTTACA	CTACCGGTCATATC	CGTCCGAATACGTC	TACTGCTAACCCCT	ACTCTCAAGTACGC	CACGGGAGAGGCGG	AATGGTAGTATTCA	CCTCGATGGAAGCT	GACTGGGCCGCAGG	TATTAGGCCTCAAT	GGCGTTAATGCGAT	CTCGAAATCTACCG	AAGCGTACACCACT	ACTATGAGACAGGT	CTCTCAACACTAGT	ACTGCAATACTTCT	AGGCACTAACCTCA	CGAGGCTGCCCGAG	AGTTAATGGCTTGC	GATGTCCCGCTTTT	ACCGC
0610005C13Rik	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
0610007P14Rik	0	0	0	0	0	0	0	0	0	0	0	0	0	2	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
0610009B22Rik	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
0610009E02Rik	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
0610009L18Rik	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
```

### `Puck*genenames_barcodes.csv` (2 files)

inspected: `SCP1348/SCP1348/other/Puck_200727_02_genenames_barcodes.csv` (963.69 KB)

delimiter: comma; columns in first line: 2
first lines:
```text
Genes,Barcodes
"['0610005C13Rik', '0610007P14Rik', '0610009B22Rik', '0610009E02Rik', '0610009L18Rik', '0610009O20Rik', '0610010F05Rik', '0610011F06Rik', '0610012D04Rik', '0610030E20Rik', '0610031O16Rik', '0610037L13Rik', '0610038B21Rik', '0610039K10Rik', '0610040B10Rik', '0610040F04Rik', '0610040J01Rik', '0610043K17Rik', '1010001B22Rik', '1010001N08Rik', '1110001J03Rik', '1110002J07Rik', '1110002L01Rik', '111000

```
line count: 2

### `Puck*matched_bead_barcodes.txt` (10 files)

inspected: `SCP1348/SCP1348/other/Puck_220408_15_matched_bead_barcodes.txt` (306.03 KB)

first lines:
```text
CGAGNACRAAGGGT
CTCCCCCGGCTCTT
GTCGGAACGATGGT
ACCTATAGCATTGT
CCGTAGACATTTCT
CCCTCCCAGATTAA
```
line count: 20,402

### `Puck*matched_bead_locations.txt` (10 files)

inspected: `SCP1348/SCP1348/other/Puck_220408_15_matched_bead_locations.txt` (320.65 KB)

delimiter: tab; columns in first line: 3
first lines:
```text
0	1540.23	2510.97
0	2839.9	2616.5
0	3575	872.59
0	929.35	2857.4
0	2007.8	1252.7
0	1205.7	1581.8
```
line count: 20,402

### `Puck*sparse_matrix.npz` (2 files)

inspected: `SCP1348/SCP1348/other/Puck_200727_02_sparse_matrix.npz` (15.76 MB)

| array | shape | dtype |
|---|---|---|
| indices.npy | (7425961,) | <i4 |
| indptr.npy | (20573,) | <i4 |
| format.npy | () | /S3 |
| shape.npy | (2,) | <i8 |
| data.npy | (7425961,) | <i8 |

### `Puck_object*.pickle` (17 files)

inspected: `SCP1348/SCP1348/other/Puck_object_2020-12-12_Puck_201014_05.pickle` (12.28 GB)

pickle protocol: 5; scanned first 8.00 MB without unpickling
classes / functions referenced: __main__.PuckReplicate, pandas.core.frame.DataFrame, pandas.core.internals.managers.BlockManager, pandas.core.indexes.base._new_Index, _new_Index.Index, numpy.core.multiarray._reconstruct, numpy.ndarray, ndarray.dtype, pandas.core.indexes.numeric.Int64Index, numpy.core.numeric._frombuffer
first short strings (attribute names, keys): __main__, PuckReplicate, puck_name, 2020-12-12_Puck_201014_05, abbrev_sample_reference, Puck_201014_05, genome, hg19, clonotype_sample_name, 210824_M00336_0898_000000000-JT4KD, clonotype_fastq_name, rln2_S1, resave_state, abbrev_rep_name, cluster_num_to_name_list, clonotype_mixcr_name, rln, cell_type_list, umi_filter_number, resave_sparse, rctd_fn, , file_type, jilong, dge_filename, spatial_barcodes_s1, spatial_locations_s1, bc_loc_dict_s1, AACAGCTTGTTAAG, AAAGCCAGAATGAC, TCAAGCCCCACCAG, TCTCCACTACTGGA, TCCTAATASCAATY, ATACGACACGTGGC, ATTGGAACCAAAGG, CTAATTTCTACTCT, GAAGCCCTGATAGT, TGAAGTTTTAGTAG, AAACCCAGCTCGAG, AGACCGAAAGGTCG, TTCCATGACCTAGA, ACACTTCTACACGA, TCGGTCGGSAGATC, CCCGCACTCAGGSC, CGGATTCANGCAGG, TAATCACGAGGGTC, AAGTRATCCTCCCT, AGACCAAACTCATT, TATSTTCTTAGCTG, AACGCTTCCTTTAC, GGCCATCGGGGGCC, ACTGTAAASTTATG, AACGMCTGTGATCA, TAACGGCGCAAACC, ATCCGCAACAAATC, AGAATGTCCAAACG, CACAAGCACTAGGA, ACCAAAGCSGCCAC, GAGTACAAACGTGA, AAGTCGCAGATTAT
note: loading this needs the original authors' Python classes; treat as untrusted code.

### `Puck_object*submit.pickle` (5 files)

inspected: `SCP1348/SCP1348/other/Puck_object_2021-09-01_Puck_210731_11_submit.pickle` (18.15 GB)

pickle protocol: 5; scanned first 8.00 MB without unpickling
classes / functions referenced: __main__.PuckReplicate, pandas.core.series.Series, pandas.core.internals.managers.SingleBlockManager, pandas.core.indexes.base._new_Index, pandas.core.indexes.range.RangeIndex, numpy.core.multiarray._reconstruct, numpy.ndarray, ndarray.dtype, builtins.slice, allows_duplicate_labels.scalar, pandas.core.frame.DataFrame, DataFrame.BlockManager, BlockManager.Index, pandas.core.indexes.numeric.Int64Index, numpy.core.numeric._frombuffer
first short strings (attribute names, keys): __main__, PuckReplicate, puck_name, 2021-09-01_Puck_210731_11_submit, abbrev_sample_reference, Puck_210731_11_submit, genome, hg19, clonotype_sample_name, 210830_M01581_1679_000000000-JT32K, clonotype_fastq_name, V39_S2, resave_state, abbrev_rep_name, cluster_num_to_name_list, clonotype_mixcr_name, V39, cell_type_list, umi_filter_number, resave_sparse, rctd_fn, , file_type, slide-seq-tools, dge_filename, spatial_barcodes_s1, AAAAAAAAAAAAAG, AAAAAAAAAAAACA, AAAAAAAAAAAACG, AAAAAAAAAAAAGC, AAAAAAAAAAAAGG, AAAAAAAAAAAAGT, AAAAAAAAAAAATG, AAAAAAAAAAACGA, AAAAAAAAAAACGG, AAAAAAAAAAACTG, AAAAAAAAAAAGCT, AAAAAAAAAAAGGA, AAAAAAAAAAAGTG, AAAAAAAAAAATAG, AAAAAAAAAAATGA, AAAAAAAAAAATGG, AAAAAAAAAAATTA, AAAAAAAAAAATTC, AAAAAAAAAAATTG, AAAAAAAAAAATTT, AAAAAAAAAACAAA, AAAAAAAAAAGAAA, AAAAAAAAAAGGCC, AAAAAAAAAAGGGG, AAAAAAAAAATAGA, AAAAAAAAAATTTG, AAAAAAAAACAAGA, AAAAAAAAACAATA, AAAAAAAAAGAAGA, AAAAAAAAAGAATA, AAAAAAAAATAAAA, AAAAAAAAATAAAT, AAAAAAAAATAACA, AAAAAAAAATAATA
note: loading this needs the original authors' Python classes; treat as untrusted code.

### `RCC_Bulk*.xls` (1 file)

inspected: `SCP1348/SCP1348/other/RCC_Bulk_TCR.26Oct20.xls` (2.85 MB)

binary: OLE2 (legacy Excel .xls / Office)

### `Supplementary_Table*.xls` (1 file)

inspected: `SCP1348/SCP1348/other/Supplementary_Table_3.xls` (222.21 KB)

binary: OLE2 (legacy Excel .xls / Office)

### `TCR_de.pdf` (1 file)

inspected: `SCP1348/SCP1348/other/TCR_de.pdf` (425.34 KB)

binary: PDF

### `adata_erv_rcc*.h5ad` (1 file)

inspected: `SCP1348/SCP1348/anndata/adata_erv_rcc_08.h5ad` (4.74 MB)

AnnData (.h5ad) summary:
X: csr_matrix, shape=(42413, 6160), nnz=56,449, dtype=float32
obs: 42413 rows, 4 columns; index '_index' (first ids: ['TCCTCGCGGCAGGA', 'AAAAAAAAAAAACA', 'AGGTCCGGCCGCTC'])
| column | dtype | first values |
|---|---|---|
| tissue | categorical (3 levels: Lung, TIL Chemokines, Tumor) | TIL Chemokines, TIL Chemokines, Tumor |
| tumor_beads | int64 | [0, 0, 1] |
| n_genes_by_counts | int64 | [20, 283, 9] |
| total_counts | float32 | [23.0, 703.0, 11.0] |
var: 6160 rows, 5 columns; index 'transcript' (first ids: ['HARLEQUIN_5q31.2', 'HARLEQUIN_1p34.1', 'HARLEQUIN_1q24.3'])
| column | dtype | first values |
|---|---|---|
| n_counts | float32 | [6672.0, 2918.0, 2750.0] |
| n_cells_by_counts | int64 | [4411, 2254, 2116] |
| mean_counts | float32 | [0.15731026232242584, 0.06879965960979462, 0.064838610589... |
| pct_dropout_by_counts | float64 | [89.59988682715205, 94.68559168179567, 95.01096361964491] |
| total_counts | float32 | [6672.0, 2918.0, 2750.0] |
obsm: spatial (42413, 2)
HDF5 tree (depth <= 3):
```text
X/ [csr_matrix]
  data  dataset shape=(56449,) dtype=float32
  indices  dataset shape=(56449,) dtype=int32
  indptr  dataset shape=(42414,) dtype=int32
obs/ [dataframe]
  __categories/
    tissue  dataset shape=(3,) dtype=object
  _index  dataset shape=(42413,) dtype=object
  n_genes_by_counts  dataset shape=(42413,) dtype=int64
  tissue  dataset shape=(42413,) dtype=int8
  total_counts  dataset shape=(42413,) dtype=float32
  tumor_beads  dataset shape=(42413,) dtype=int64
obsm/
  spatial  dataset shape=(42413, 2) dtype=float64
var/ [dataframe]
  mean_counts  dataset shape=(6160,) dtype=float32
  n_cells_by_counts  dataset shape=(6160,) dtype=int64
  n_counts  dataset shape=(6160,) dtype=float32
  pct_dropout_by_counts  dataset shape=(6160,) dtype=float64
  total_counts  dataset shape=(6160,) dtype=float32
  transcript  dataset shape=(6160,) dtype=object
```

### `barcodes.csv` (1 file)

inspected: `SCP1348/SCP1348/other/barcodes.csv` (164.86 KB)

delimiter: comma; columns in first line: 13
first lines:
```text
"SCC180161SD_AAACGGGAGATGCGAC","SCC180161SD_AAAGATGGTGTCCTCT","SCC180161SD_AAAGATGTCCGTCAAA","SCC180161SD_AAATGCCCACCAGGTC","SCC180161SD_AACCATGCATCTCGCT","SCC180161SD_AACCATGTCTAACTGG","SCC180161SD_AACTCTTTCTGTCTAT","SCC180161SD_AACTTTCAGGTCATCT","SCC180161SD_AAGACCTAGTTAGCGG","SCC180161SD_AAGGCAGAGGCGATAC","SCC180161SD_AAGGTTCTCGACAGCC","SCC180161SD_AAGTCTGGTTAAGTAG","SCC180161SD_AATCCAGAGATTACC

```
line count: 1

### `celltype.csv` (1 file)

inspected: `SCP1348/SCP1348/other/celltype.csv` (65.22 KB)

delimiter: comma; columns in first line: 41
first lines:
```text
"B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells","B-cells",

```
line count: 1

### `cfg*.txt` (1 file)

inspected: `SCP1348/cfg_20261101_2038.txt` (128.05 KB)

download config with signed URLs; content intentionally not shown

### `cfg.txt` (1 file)

inspected: `SCP1348/cfg.txt` (128.05 KB)

download config with signed URLs; content intentionally not shown

### `cloneids_readids*.pickle` (1 file)

inspected: `SCP1348/SCP1348/other/cloneids_readids_2020-08-31_Puck_200727_02.pickle` (717.76 MB)

pickle protocol: 5; scanned first 8.00 MB without unpickling
classes / functions referenced: pandas.core.frame.DataFrame, pandas.core.internals.managers.BlockManager, functools.partial, pandas.core.internals.blocks.new_block, numpy.core.numeric._frombuffer, numpy.dtype, numpy.core.multiarray._reconstruct, _reconstruct.ndarray, pandas.core.indexes.base._new_Index, _new_Index.Index, pandas.core.indexes.numeric.Int64Index
first short strings (attribute names, keys): pandas.core.frame, DataFrame, _mgr, pandas.core.internals.managers, BlockManager, functools, partial, pandas.core.internals.blocks, new_block, ndim, numpy.core.numeric, _frombuffer, numpy, dtype, f8, <, C, i8, numpy.core.multiarray, _reconstruct, ndarray, O8, |, TGTGCCAGCTCTCGGGCCATTTATGAACAGTACTTC, TGTGCCAGCTCTCGGGCCAATTATGAACAGTTCTTC, TGTGCAGCAAGTGACAACTATCAGTTGTTCTGG, TGTGCAGCAAGTGACAACTTTCAGTTGATCTGG, CGTGCCAGCTCTCGGGCCACTTATGAACAGTACTTC, TGTGCCAGCCCTCGGGCCAATTATGAACAGTGCTTC, TGTGCCAGCTCTCGGGCCAATTATGGTCAGTACTTC, TGTGCAGCAAGTGGCAACTATCAGTTGGTCTGG, TGCGCAGCAAGTGTCAACTATCAGTTGATCTGG, TGTGCAGCAAGTGACAACTGTCAGTTGGTCTGG, TGTGCAGCAAGTGGCAACTGTCAGTTGATCTGG, TGTGCAGCAGGTGACAACTATCAGTTGGTCTGG, TGTGCAGCAAGTGGCATCTATCAGTTGATCTGG, TGGGCCAGCTCTCGGGCCAATTACGATCAGTACTTC, TGTGCAGGACTAACAGGCAAAACCGGAAAACTCATCTTT, TGTGCAGCAAGTGCCGGCTGGCAAGGCACTGGGTCTAAGCTGTCATTT, CTTCTGTGCCTCTCGGGCCGATTATGAACAGTACTTCGGTCCCG, TGTGCTATGAGATTC, TGCGCCTCTCGGAAACGCTGAGGAGGTTT, TGTGCTATGGGGGGGGTTACAGAACTTCTATTCT, HHHHHHHHGHHHHGGGGGGHHHHHHHHHHHHHHHHH, HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH, HGHGGHGHGHHHHGGGGGFFGHFHHGGGGGHGGHHH, GHGGHHGHGGGHHGGGGGEGGHHGHGGGHHGGFHHH, HHHHHHHHGGHHGEGGGGBBGGGGHHFHFGHHGHHH, HHHHHGGHGGGGGHGHFGHFGHFFGHHHEGHHH, HHHGGEEEGGHGHHHHHHHHGHGHHHHEFGHGH, HHHHHHHHHGHHHGGGFHHHHHEFGFHGFHHHH, HHHHHHHHHHHHGFGGHHGGHHGGFHHGHHHHH, HHHHHHHHGGHGFHHFHHGGHGEFFHHHEHHHH, HHHHHHHHHGHHHHGGGHHFHHHHFHHFHHHHH, HHFHHHEHFHHHHGGGGGEFGHBDFF???EDFGHHH, HGFHHFHA?CGHBGFGGFGFFHHFCGBBCHHHHBGHHGG, GGFHGFHBHFHGFFHGGFFCGGHHFGHFGGFEABFFDDFFHHHH?GHH, [[W[&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&[[U[[[[, AAAAAAAAAAAAAAA, AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
note: loading this needs the original authors' Python classes; treat as untrusted code.

### `dge.csv` (1 file)

inspected: `SCP1348/SCP1348/other/dge.csv` (290.10 MB)

delimiter: comma; columns in first line: 128
first lines:
```text
0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,12
0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,
```
line count: 5,319

### `file_supplemental_info.tsv` (1 file)

inspected: `SCP1348/SCP1348/file_supplemental_info.tsv` (10.66 KB)

delimiter: tab; columns in first line: 11
first lines:
```text
filename	file_type	species_scientific_name	genome_assembly_name	genome_assembly_accession	genome_annotation_name	is_raw_counts	library_preparation_protocol	units	biosample_input_type	modality
Puck_200727_02.digital_expression.txt	Other									
Puck_200727_08.digital_expression.txt	Other									
Puck_200727_09.digital_expression.txt	Other									
Puck_200727_10.digital_expression.txt	Other									
Puck_200727_12.digital_expression.txt	Other									
```
line count: 212

### `genes.csv` (1 file)

inspected: `SCP1348/SCP1348/other/genes.csv` (119.71 KB)

delimiter: comma; columns in first line: 41
first lines:
```text
"FO538757.2","AP006222.2","RP11-206L10.9","LINC00115","NOC2L","KLHL17","RP11-54O7.17","HES4","ISG15","AGRN","C1orf159","TNFRSF18","TNFRSF4","SDF4","B3GALT6","UBE2J2","ACAP3","PUSL1","CPSF3L","CPTP","DVL1","MXRA8","AURKAIP1","CCNL2","MRPL20","ANKRD65","RP4-758J18.10","VWA1","ATAD3C","ATAD3B","ATAD3A","SSU72","RP5-832C2.5","C1orf233","RP11-345P4.9","MIB2","MMP23B","CDK11B","SLC35E2B","CDK11A","SLC35

```
line count: 1

### `lymph_rctd.csv` (1 file)

inspected: `SCP1348/SCP1348/other/lymph_rctd.csv` (7.69 MB)

delimiter: comma; columns in first line: 23
first lines:
```text
,B,DC,Endothelial,ILC,Monocytes,MP,NK,T_CD4+,T_CD8+,Treg,class_max_wieght,xcoord,ycoord,spot_class,first_type,second_type,first_class,second_class,min_score,singlet_score,conv_all,conv_doublet
AAGTACATCTGATT,0.833878107245673,0.140249949086893,0.0176058502277305,6.38950656391937e-05,6.38950656391943e-05,6.38950656391969e-05,6.38950656400085e-05,0.007820774491896,6.38950656724086e-05,0.0001258436195773,B,1961.3,1972.7,singlet,B,Endothelial,False,False,531.297889731439,538.676183766217,True,True
CGTASCCCTTCGCG,0.64239337110217,0.047719517143909,0.0277634280753483,0.0001306320801584,0.0025305591706564,0.0008851659244666,0.0001306320801706,0.0001306320801584,0.0001306320801583,0.278185430262804,B,4245.35,2243.1,singlet,B,Treg,False,False,554.388785933616,576.823867444897,True,True
ACTCCTAGCCTTTA,0.681972927108436,0.178018160552542,0.0271736794371733,0.0001583961475163,0.0001583961475167,0.0185443938894542,0.0001583961485379,0.0001583961475167,0.0001583961470713,0.0934988582742349,B,4189.5,2628.5,singlet,B,DC,False,False,537.560416483148,556.006925531525,True,True
CTCGCGGCTAGCAC,0.681000358602835,0.162459805365275,0.0064062044876357,9.12034506073798e-05,0.0004847411444387,0.0328566114547153,9.12034506811573e-05,0.109575107686406,0.0069435609067975,9.12034506073823e-05,B,745.13,2284.8,doublet_uncertain,B,DC,False,False,563.666969915048,602.307897019632,True,True
TATGCGGGGGATTA,0.718207424286247,0.129405631054834,0.0039663671631583,6.38561588683465e-05,6.38561590904352e-05,0.026363031483462,6.38561602600387e-05,6.38561590902251e-05,6.38561588280997e-05,0.121738265216162,B,1926.1,4627.7,singlet,B,DC,False,False,517.163558618631,538.306582291119,True,True
```
line count: 26,028

### `mel_mtx.mtx` (1 file)

inspected: `SCP1348/SCP1348/other/mel_mtx.mtx` (262.35 MB)

delimiter: space; columns in first line: 5
first lines:
```text
%%MatrixMarket matrix coordinate real general
%
5318 13616 10905597
1 40 1.0000000e+00
1 89 1.0000000e+00
1 234 1.0000000e+00
```
line count: 10,905,600

### `mel_ref.h5ad` (1 file)

inspected: `SCP1348/SCP1348/anndata/mel_ref.h5ad` (302.34 MB)

AnnData (.h5ad) summary:
X: dense, shape=(5318, 13616), dtype=float32
obs: 5318 rows, 11 columns; index '_index' (first ids: ['SCC180161SD_AAACGGGAGATGCGAC', 'SCC180161SD_AAAGATGGTGTCCTCT', 'SCC180161SD_AAAGATGTCCGTCAAA'])
| column | dtype | first values |
|---|---|---|
| Condition | categorical (2 levels: Cryopreserved Cell Suspension, Cry... | Cryopreserved Cell Suspension, Cryopreserved Cell Suspens... |
| CellType | categorical (5 levels: B-cells, CAFs, Cancer, Monocytes/M... | B-cells, B-cells, B-cells |
| ClusterID | categorical (7 levels: 0, 4, 6, 12, 13, 15, 17) | 13, 13, 13 |
| n_genes_by_counts | int32 | [402, 936, 755] |
| total_counts | float32 | [1073.0, 3033.0, 1907.0] |
| prefix | categorical (2 levels: SCC180161ND, SCC180161SD) | SCC180161SD, SCC180161SD, SCC180161SD |
| total_counts_mt | float32 | [57.0, 218.0, 168.0] |
| pct_counts_mt | float32 | [5.312208652496338, 7.187602519989014, 8.809648513793945] |
| leiden | categorical (15 levels: 0, 1, 2, 3, 4, 5, 6, 7) | 9, 9, 9 |
| Tstate | categorical (2 levels: T, nonT) | nonT, nonT, nonT |
| Cell | categorical (6 levels: B cell, CD4 T cell, CD8 T cell, Fi... | B cell, B cell, B cell |
var: 13616 rows, 12 columns; index 'gene' (first ids: ['FO538757.2', 'AP006222.2', 'RP11-206L10.9'])
| column | dtype | first values |
|---|---|---|
| n_cells | int64 | [893, 150, 214] |
| n_cells_by_counts | int64 | [2733, 483, 765] |
| mean_counts | float32 | [0.33267486095428467, 0.04507497698068619, 0.075154885649... |
| pct_dropout_by_counts | float64 | [75.46017778575917, 95.66310496543055, 93.13100475891174] |
| total_counts | float32 | [3705.0, 502.0, 837.0] |
| mt | bool | [False, False, False] |
| highly_variable | bool | [False, False, False] |
| means | float64 | [0.2757060409766295, 0.04087397058783292, 0.0710604196968... |
| dispersions | float64 | [1.3537487245291129, 0.8982019951173522, 1.0733634447296263] |
| dispersions_norm | float32 | [0.21139582991600037, -0.8248133659362793, -0.42638245224... |
| mean | float64 | [0.1754910719667218, 0.025792425925727967, 0.043430507394... |
| std | float64 | [0.36608839850122354, 0.14023757351211832, 0.187831720214... |
obsm: X_pca (5318, 50); X_umap (5318, 2)
varm: PCs (13616, 50)
obsp: connectivities (group); distances (group)
uns keys (11): CellType_colors, ClusterID_colors, Condition_colors, Tstate_colors, hvg, leiden, leiden_colors, neighbors, pca, rank_genes_groups, umap
HDF5 tree (depth <= 3):
```text
X  dataset shape=(5318, 13616) dtype=float32
obs/ [dataframe]
  Cell  dataset shape=(5318,) dtype=int8
  CellType  dataset shape=(5318,) dtype=int8
  ClusterID  dataset shape=(5318,) dtype=int8
  Condition  dataset shape=(5318,) dtype=int8
  Tstate  dataset shape=(5318,) dtype=int8
  __categories/
    Cell  dataset shape=(6,) dtype=object
    CellType  dataset shape=(5,) dtype=object
    ClusterID  dataset shape=(7,) dtype=object
    Condition  dataset shape=(2,) dtype=object
    Tstate  dataset shape=(2,) dtype=object
    leiden  dataset shape=(15,) dtype=object
    prefix  dataset shape=(2,) dtype=object
  _index  dataset shape=(5318,) dtype=object
  leiden  dataset shape=(5318,) dtype=int8
  n_genes_by_counts  dataset shape=(5318,) dtype=int32
  pct_counts_mt  dataset shape=(5318,) dtype=float32
  prefix  dataset shape=(5318,) dtype=int8
  total_counts  dataset shape=(5318,) dtype=float32
  total_counts_mt  dataset shape=(5318,) dtype=float32
obsm/
  X_pca  dataset shape=(5318, 50) dtype=float32
  X_umap  dataset shape=(5318, 2) dtype=float32
obsp/
  connectivities/ [csr_matrix]
    data  dataset shape=(214428,) dtype=float32
    indices  dataset shape=(214428,) dtype=int32
    indptr  dataset shape=(5319,) dtype=int32
  distances/ [csr_matrix]
    data  dataset shape=(145956,) dtype=float64
    indices  dataset shape=(145956,) dtype=int32
    indptr  dataset shape=(5319,) dtype=int32
uns/
  CellType_colors  dataset shape=(5,) dtype=object
  ClusterID_colors  dataset shape=(7,) dtype=object
  Condition_colors  dataset shape=(2,) dtype=object
  Tstate_colors  dataset shape=(2,) dtype=object
  hvg/
    flavor  dataset shape=() dtype=object
  leiden/
    params/
  leiden_colors  dataset shape=(15,) dtype=object
  neighbors/
    connectivities_key  dataset shape=() dtype=object
    distances_key  dataset shape=() dtype=object
    params/
  pca/
    params/
    variance  dataset shape=(50,) dtype=float32
    variance_ratio  dataset shape=(50,) dtype=float32
  rank_genes_groups/
    names  dataset shape=(13666,) dtype=[('T', 'O')]
    params/
    scores  dataset shape=(13666,) dtype=[('T', '<f4')]
  umap/
    params/
var/ [dataframe]
  dispersions  dataset shape=(13616,) dtype=float64
  dispersions_norm  dataset shape=(13616,) dtype=float32
  gene  dataset shape=(13616,) dtype=object
  highly_variable  dataset shape=(13616,) dtype=bool
  mean  dataset shape=(13616,) dtype=float64
  mean_counts  dataset shape=(13616,) dtype=float32
  means  dataset shape=(13616,) dtype=float64
  mt  dataset shape=(13616,) dtype=bool
  n_cells  dataset shape=(13616,) dtype=int64
  n_cells_by_counts  dataset shape=(13616,) dtype=int64
  pct_dropout_by_counts  dataset shape=(13616,) dtype=float64
  std  dataset shape=(13616,) dtype=float64
  total_counts  dataset shape=(13616,) dtype=float32
varm/
  PCs  dataset shape=(13616, 50) dtype=float64
```

### `monocyte_de_genes.csv` (1 file)

inspected: `SCP1348/SCP1348/other/monocyte_de_genes.csv` (329.59 KB)

delimiter: comma; columns in first line: 10
first lines:
```text
"","tau","log_fc_est","sd_est","Z_est","p_cross","ct_prop","expr","q_val","p"
"AATF",0.407490380381908,-0.0721318826883252,0.213305894670489,-0.33816169402985,0.043852487884907,0.707810203779312,4.63249445734724e-05,0.912284970964443,0.735241340898873
"ABCB4",0,-0.831445685136246,0.439343961702075,-1.89247095126816,0.276801883690686,0.694456345007776,3.44643733719696e-06,0.298827123190767,0.0584282604682337
"ABHD12",0,0.0917874481138916,0.104349454740574,0.879615982106346,0.945054243076142,0.774718117584453,8.26232014362232e-05,0.719632990782994,0.379067377927034
"ABI1",0,-0.0643956223247702,0.0886499352747055,-0.726403489469261,0.184400831465887,0.821313600910792,8.54972448918047e-05,0.774283609482996,0.467591452654814
"ABR",0,0.229622294849914,0.109620692394209,2.09469845368395,0.763082425083945,0.704967197192148,6.05382852411004e-05,0.236262510341916,0.0361978067887664
```
line count: 2,057

### `nUMI.csv` (1 file)

inspected: `SCP1348/SCP1348/other/nUMI.csv` (49.35 KB)

delimiter: comma; columns in first line: 45
first lines:
```text
"1073.0","3033.0","1907.0","2255.0","2540.0","3719.0","19340.0","3466.0","5048.0","2662.0","2165.0","813.0","3778.0","2802.0","3622.0","1113.0","3048.0","2966.0","2661.0","1396.0","2624.0","2282.0","3869.0","2151.0","1722.0","2440.0","1403.0","898.0","3938.0","1251.0","4148.0","2126.0","700.0","2246.0","5627.0","4804.0","2457.0","2925.0","801.0","2646.0","2751.0","3039.0","2673.0","2860.0","2530.0

```
line count: 1

### `new_format*.h5ad` (3 files)

inspected: `SCP1348/SCP1348/anndata/new_format_2020-09-02_Puck_200727_10.h5ad` (3.88 GB)

AnnData (.h5ad) summary:
X: dense, shape=(36228, 26717), dtype=float32
obs: 36228 rows, 4 columns; index '_index' (first ids: ['CTACAGATCAAATC', 'GCCTTCAAGCTCAA', 'GCTTGTAGTGGATC'])
| column | dtype | first values |
|---|---|---|
| x | float64 | [5234.2, 5031.2, 4706.8] |
| y | float64 | [3893.0, 3441.0, 4342.4] |
| alpha | categorical (179 levels: ['CAAKAGGYQKVTF'], ['CAASFANAGNM... | ['CAASIRG_GFQKLVF'], ['NA'], [] |
| beta | categorical (674 levels: ['CAIPRDRGLSGEQYF', 'CAIPRDRGLSG... | [], ['NA'], ['CASRGQGGYNSPLHF'] |
var: ? rows, 0 columns; index '_index' (first ids: ['A1BG', 'A1BG-AS1', 'A1CF'])
| column | dtype | first values |
|---|---|---|
HDF5 tree (depth <= 3):
```text
X  dataset shape=(36228, 26717) dtype=float32
obs/ [dataframe]
  __categories/
    alpha  dataset shape=(179,) dtype=object
    beta  dataset shape=(674,) dtype=object
  _index  dataset shape=(36228,) dtype=object
  alpha  dataset shape=(36228,) dtype=int16
  beta  dataset shape=(36228,) dtype=int16
  x  dataset shape=(36228,) dtype=float64
  y  dataset shape=(36228,) dtype=float64
var/ [dataframe]
  _index  dataset shape=(26717,) dtype=object
```

### `post_treatment_clonotype_fraction_slide_seq.csv` (1 file)

inspected: `SCP1348/SCP1348/other/post_treatment_clonotype_fraction_slide_seq.csv` (61.57 KB)

delimiter: comma; columns in first line: 4
first lines:
```text
,clonotype,fraction,name
0,CASSQGLAGVLGQFF,0.044961461604339135,TCR-1
1,CSARDPGPDTQYF,0.043105909220667996,TCR-2
2,CASRVQGGPGANVLTF,0.03197259491864116,TCR-3
3,CASSPRTSGRYNEQFF,0.030117042534970027,TCR-4
4,CASSPYHSSGGETQYF,0.02569226377390808,TCR-5
```
line count: 1,224

### `pre_treatment_clonotype_fraction_slide_seq.csv` (1 file)

inspected: `SCP1348/SCP1348/other/pre_treatment_clonotype_fraction_slide_seq.csv` (1.99 KB)

delimiter: comma; columns in first line: 4
first lines:
```text
,clonotype,fraction,name
0,CASSMGTAYEQYF,0.5887096774193549,TCR-1224
1,CASSSTSGDRNEQFF,0.07258064516129033,TCR-1225
2,CASSIDYNEQFF,0.06854838709677419,TCR-1226
3,CASSRGAASYNEQFF,0.028225806451612902,TCR-1227
4,CASNLRGAGDNEQFF,0.028225806451612902,TCR-1228
```
line count: 42

### `rcc*five_cells.csv` (1 file)

inspected: `SCP1348/SCP1348/other/rcc_08_five_cells.csv` (287.08 KB)

delimiter: comma; columns in first line: 9
first lines:
```text
barcodes,xcoord,ycoord,tissue,tumor_beads,n_counts,n_genes_by_counts,total_counts,Cell Types
AGGTCCGGCCGCTC,2581.9,5379.9,Tumor,1,2.0,1,2.0,Macrophage
CTCCAGGCTAGTTC,1971.4,3674.2,Tumor,1,3.0,1,3.0,Endothelial
AATCCACCCCTCGA,3600.2,5141.4,Tumor,1,2.0,1,2.0,Macrophage
AGGGGCTGGACATC,2052.1,4938.6,Tumor,1,2.0,1,2.0,Endothelial
CATCAGTGCCGACT,1840.7,4466.8,Tumor,1,3.0,1,3.0,Macrophage
```
line count: 5,137

### `rcc*harl.csv` (1 file)

inspected: `SCP1348/SCP1348/other/rcc_08_harl.csv` (388.35 KB)

delimiter: comma; columns in first line: 6
first lines:
```text
,tumor_beads,n_genes_by_counts,total_counts,xcoord,ycoord
TCCTCGCGGCAGGA,0,8,23.0,3283.6,2346.0
AAAAAAAAAAAACA,0,18,703.0,2389.7,1795.1
AGGTCCGGCCGCTC,1,4,11.0,2581.9,5379.9
AGCACAATCCATGG,0,6,15.0,3045.6,1373.4
CTCCAGGCTAGTTC,1,6,28.0,1971.4,3674.2
```
line count: 10,472

### `rcc*rcc_cells.csv` (5 files)

inspected: `SCP1348/SCP1348/other/rcc_10_rcc_cells.csv` (308.58 KB)

delimiter: comma; columns in first line: 12
first lines:
```text
barcode,n_genes_by_counts,log1p_n_genes_by_counts,total_counts,log1p_total_counts,tissue,tumor_beads,spot_class,first_type,second_type,xcoord,ycoord
ATCAGCCCCTAAGT,1793,7.492203042618741,3650.0,8.202756,Tumor,1,singlet,cycRCC,Endothelial,4387.3,2601.4
TACACCCCCTGCTG,1670,7.421177528595393,3325.0,8.109526,Tumor,1,singlet,RCC2,RCC1,4803.3,2767.9
ATACGGGGTGTTAC,1599,7.3777589082278725,3184.0,8.066208,Tumor,1,singlet,RCC2,Endothelial,5037.3,3892.3
TGAGTAATTTTATG,1382,7.232010331664759,2819.0,7.9444923,Tumor,1,singlet,RCC2,CD4 T cell,3812.1,3412.0
TCCTCGGGATCCAA,1500,7.313886831633462,2913.0,7.977282,Tumor,1,singlet,cycRCC,Endothelial,4508.8,2057.6
```
line count: 3,181

### `rcc_rctd_clusters*.csv` (5 files)

inspected: `SCP1348/SCP1348/documentation/rcc_rctd_clusters_2020-09-02_Puck_200727_12.csv` (575.69 KB)

delimiter: comma; columns in first line: 3
first lines:
```text
"x","y","cell_label"
3611.2,1595.4,"TumorCell_CA9"
3927.7,1628.9,"TumorCell_CA9"
738.3,3277,"TumorCell_CA9"
1388.2,2638.5,"TumorCell_CA9"
1435.8,3364.4,"TumorCell_CA9"
```
line count: 19,297

### `readIDtobarcode_dict*.pickle` (1 file)

inspected: `SCP1348/SCP1348/other/readIDtobarcode_dict_2020-08-31_Puck_200727_02.pickle` (1.71 GB)

pickle protocol: 5; scanned first 8.00 MB without unpickling
first short strings (attribute names, keys): M00136:340:000000000-CYW3P:1:1101:16426:1395, TCCCTTGGGTTGCG, TGACAAGCA, M00136:340:000000000-CYW3P:1:1101:14718:1398, AAAAAAAAAAAAAA, AAAAAAAAA, M00136:340:000000000-CYW3P:1:1101:16212:1400, CGACACGTCTCCAA, ATACACCAC, M00136:340:000000000-CYW3P:1:1101:15092:1400, CACAACTATGCTAT, ATCCGAACC, M00136:340:000000000-CYW3P:1:1101:17074:1401, AGACCGATTGTCGG, TGTTTAAAA, M00136:340:000000000-CYW3P:1:1101:15849:1402, M00136:340:000000000-CYW3P:1:1101:14643:1403, ATTCACTACTCCTG, ACAGAGAGC, M00136:340:000000000-CYW3P:1:1101:16527:1403, ATGACAGCAGATCG, GAGGAGCAC, M00136:340:000000000-CYW3P:1:1101:14473:1406, GAGCGCCATGCCTA, TTCATGGGC, M00136:340:000000000-CYW3P:1:1101:16904:1407, CCGCTGGGTTACTG, TGTTAAAGG, M00136:340:000000000-CYW3P:1:1101:14517:1407, AGGAAGATCTAGAT, AAGAGCACA, M00136:340:000000000-CYW3P:1:1101:16543:1408, M00136:340:000000000-CYW3P:1:1101:15391:1408, AGTACAGTTAAGTT, AGGGGGAGA, M00136:340:000000000-CYW3P:1:1101:15314:1410, GTCCTTCGTTCAAG, GCCGCGAAG, M00136:340:000000000-CYW3P:1:1101:17180:1410, M00136:340:000000000-CYW3P:1:1101:14351:1411, M00136:340:000000000-CYW3P:1:1101:15798:1411, M00136:340:000000000-CYW3P:1:1101:16653:1411, GGCTACGTTGCCCT, GCATGTTGG, M00136:340:000000000-CYW3P:1:1101:16925:1412, M00136:340:000000000-CYW3P:1:1101:16705:1414, ATCTTCCGGTCGTC, AATTTTTTT, M00136:340:000000000-CYW3P:1:1101:16680:1416, TCAATCCCCCTCCA, CGTCCGCCT, M00136:340:000000000-CYW3P:1:1101:15899:1416, CCCAACGACATCTA, TGCAGCCCA, M00136:340:000000000-CYW3P:1:1101:14838:1416, M00136:340:000000000-CYW3P:1:1101:16890:1416, CCCGGGTCCGCGCC, CTCGTAGCA, M00136:340:000000000-CYW3P:1:1101:14420:1417, TGAACCGGCGTCCC
note: loading this needs the original authors' Python classes; treat as untrusted code.

### `rln_paired_cloneID.txt` (1 file)

inspected: `SCP1348/SCP1348/other/rln_paired_cloneID.txt` (85.93 MB)

delimiter: tab; columns in first line: 8
first lines:
```text
descrsR2	descrsR1	cloneId	readId	targetSequences	topChains	chains	cloneMapping
M00336:898:000000000-JT4KD:1:1102:14706:1398 2:N:0:TGCTCTAC+CGATGCTT	M00336:898:000000000-JT4KD:1:1102:14706:1398 1:N:0:TGCTCTAC+CGATGCTT	-1	20	ACCTTTTCCTCTCCGCTTCACAACTGGGGGACTCAGCAATGTACTTCTGTGCAATGAGTGGGCCTGCAGGCAAATCCACCTTTGGGGATGGGACTACGCTCACTGTGAGGCCCACTCTCCAGCACCCTGACCCTGCCGTGTACCAGCTGAGAGACTCTAACTCCAGTGACAAGTCTGTCTGCCTATTCCCCGATTTTGCTTCTCAAACCAATGTGTCACACAGTAAGGATTCTGATGTGTATATCCCC,ACTGGAT
M00336:898:000000000-JT4KD:1:2109:6949:21007 2:N:0:TGCTCTAC+CGATGCTT	M00336:898:000000000-JT4KD:1:2109:6949:21007 1:N:0:TGCTCTAC+CGATGCTT	-1	3729738	GAGAACTCTCTTCAGCGTTCCCGAGAGTATGAGGCTCTGCATTTTTTT,CTTATTAAAATGGTCCCCAACATGTCTGAGCTGGAGCTTCAGTTTTCACAGGTCTCAGGTGATGCTGATGCTACTGGTCTCTGGGTCACACTTTAAAGAGGAAGACATTAGATAAAGTAAAAGGAGTCATGAGAAAAGGTGCACCTAAAAAACATCACATAACAAAATACTAAAGTCACTAGTGGAGAATAACAAACATCCC
M00336:898:000000000-JT4KD:1:1102:17151:1420 2:N:0:TGCTCTAC+CGATGCTT	M00336:898:000000000-JT4KD:1:1102:17151:1420 1:N:0:TGCTCTAC+CGATGCTT	-1	33	CCGAAGCTTGAGGATTCAGCAGTGTGTTTGTGTGCCAGCAGCCATGCCTACACTGAAGCTTTCTTTGGACACGGCACCAGACTCACAGTTGTCGAGGACCTGAACAAGGTGTTCCCAACCGAGGTCGCTGTGTTTGAGCCATCAGAAGCCGAGATCTCCCACACCCAAACGGCCACACTGGTGTGCCTGGCCACAGGCTTCTTCCCTGACCACGTGGAGCTGAGCTGTGGGTGAATGGGAGGGGGGGG,AAAAAAA
M00336:898:000000000-JT4KD:1:2114:16961:7435 2:N:0:TGCTCTAC+CGATGCTT	M00336:898:000000000-JT4KD:1:2114:16961:7435 1:N:0:TGCTCTAC+CGATGCTT	-1	4118053	ATCCAGCCCTCAGAACCCAGGGACTCAGCTGTGTACTTCTGTGCCAGCAGTTTAGTTTTGGCAGGGGGGCCCAGATTCGGCTACACCTTCGGTTCGGGGACCAGGTTAACCGTTGTAGAGGACCTGAACAAGGTGTTCCCACCCGAGGTCGCTGTGTTTGAGCCATCAGAGGCAGAGATCTCCCACACCCACAAGGCCACCCTGGGGTGCCTGGCCACAAGCTTCTTCCCTGACCACGTGGAGCTGGG,AA
M00336:898:000000000-JT4KD:1:1102:17909:1621 2:N:0:TGCTCTAC+CGATGCTT	M00336:898:000000000-JT4KD:1:1102:17909:1621 1:N:0:TGCTCTAC+CGATGCTT	-1	213	CCCCAACCAGACCTCTCTGTACCTCTGTGCCAGCATTCCGACAGGGTTTCATCAGCCCCAGCATGGTGGAGAGGGGACTCGACTCTCCATCCTCGCGGCCCTGAACAAGGGGTTCCCACCCGCGGTCGCTGTGTTTGAGCCATCAGAAGCAGGGATCTCCCCCACCCAAAGGCCCACACTGGTGTGCCTGGCCACCGGCTTCTTCCCTGACCACGTTGATCTGAGCTGGTGGGGAAATGGGGAGGGGG,AAAAAA
```
line count: 184,338

### `rln_paired_clones.txt` (1 file)

inspected: `SCP1348/SCP1348/other/rln_paired_clones.txt` (1.71 MB)

delimiter: tab; columns in first line: 28
first lines:
```text
cloneId	cloneCount	cloneFraction	targetSequences	targetQualities	allVHitsWithScore	allDHitsWithScore	allJHitsWithScore	allCHitsWithScore	allVAlignments	allDAlignments	allJAlignments	allCAlignments	nSeqImputedFR1	minQualFR1	nSeqImputedCDR1	minQualCDR1	nSeqImputedFR2	minQualFR2	nSeqImputedCDR2	minQualCDR2	nSeqImputedFR3	minQualFR3	nSeqImputedCDR3	minQualCDR3	nSeqImputedFR4	minQualFR4	aaSeqImputedFR1
0	668.0	0.015945384670470006	TGCAGCTACTCAACCTGGTATCGACAAGACCCAGGCAAAGCCCCCAAACTCTTGATTTATGATGTCACTAGTCGGCCCTCAGGGGTTTCTAATCGCTTCTCTGGCTCCAAGTCTGGCAACACGGCCTCCCTGACCATCTCTGGGCTCCAGGCTGAGGACGAGGCTGATTATTACTGCAGCTCATATACAAGCAGCAGCACTGTGCTATTCGGCGGAGGGACCAAGCTGACCGTCCTAGGTCAGCCCAAGGCTGCCCCCTCGG,CCCCCCTCGGAGGGCTTCAAGCCAAACAAGCCCCCCTGG	[[[[[[[[['[[&345022101134[//745885.99568/5652443699/9<2455/1=4490420
1	530.0	0.012651278256510634	GCATCCTGCACATCACAGCCCCTAAACCTGAAGACTCAGCCACTTATCTCTGTGCTGTGCAATTTTCTTCTGGTTCTGCAAGGCAACTGACCTTTGGATCTGGGACACAATTGACTGTTTTACCTGGTAGGCTGCCTCAATTAAATACTATTTGCACTGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	[[[[[48;5349952573/0.010:037.67@8<8:<[3?[[97:97<;?+++++++++++++++++++++++++++++++++++++++++++++[[[<<2[5[<:=[[=
2	458.0	0.010932614040531832	ACAAGACAGCCAAACATTTCTCCCTGCACATCACAGAGACCCAACCTGAAGACTCGGCTGTCTACTTCTGTGCAGCAAGTAAAGTGCAAACTGGGGCAAACAACCTCTTCTTTGGGACTGGAACGAGACTCACCGTTATTCCCTGTAAGTCCTTACCTCTTGACAAAAAAGCTCTTAGTCTGTAATGACAAGTTCTCACATCCCAGACACCTAATGAATTTCTAAATGAGCTTCCATGTGTTAAACTGATAAAACTCTCTAGGGAAAAAAAAAAAAAAAAAAA	6;;;7675362[[7;<44310//0459[?:88:6<><4967?<557>[99[<?18=[67[0[:>;6:;'''''''''''''''''''
3	426.0	0.010168763277874585	TGCACAGTGATTCAGCCACCTACCTCTGTGTGGTGAACCCCGACAGCAGTGCTTCCAAGATAATCTTTGGATCAGGGACCAGACTCAGCATCTGGCCATGTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	[[[[5587683[997=;[[859[95=,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,[8;>[?[[[;[<>[<?:;[>;;8[[[<:?:7:56>>7[???6??
4	424.0	0.010121022605208507	ATCCAGCCCTCAGAACCCAGGGACTCAGCTGTGTACTTCTGTGCCAGCAGTTACGGATCCGGGGAGCTGTTTTTTGGAGAAGGCTCTAGGCTGACCGTACTGGAGGACCTGAAAAACGTGTTCCCACCCGAGGTCGCTGTGTTTGAGCCATCAGAAGCAGAGATCTCCCACACCCAAAAGGCCACACTGGTGTGCCTGGCCACAGGCTTCTACCCCGACCAC,GAGCTGGTGGGTGAATGGGAAGGAGG	,/101//421711112183[:3244:0:[6:[:75[49:&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&;[/[.-:[;3>41[>:9[187[50>?[>-[>.9:590//.-24,18
```
line count: 1,515

### `spleen_rctd_clusters_aging.csv` (1 file)

inspected: `SCP1348/SCP1348/other/spleen_rctd_clusters_aging.csv` (313.76 KB)

delimiter: comma; columns in first line: 3
first lines:
```text
"x","y","cell_label"
2429.7,2102.8,"CD8 macrophage"
3184.9,1236.9,"B cell"
3730.9,1631.9,"CD8 macrophage"
2926.4,3099,"B cell"
3750.5,1843.6,"CD8 macrophage"
```
line count: 11,886

### `tcr_de_genes.csv` (1 file)

inspected: `SCP1348/SCP1348/other/tcr_de_genes.csv` (288.98 KB)

delimiter: comma; columns in first line: 10
first lines:
```text
"","tau","log_fc_est","sd_est","Z_est","p_cross","ct_prop","expr","q_val","p"
"AAK1",0,0.756509458716712,0.557861348460312,1.35608867831526,0.642768340141751,1,0.00014028467317721,0.417329175148728,0.175070954683038
"AAMP",0.435338665246406,1.34041406789804,0.682582535982798,1.96373917766308,0.415827324802489,0.510054463431988,6.8063248726862e-05,0.234952754969783,0.0495603467514386
"AATF",0,0.559239658663682,0.435466300383062,1.28423177217558,0.943103978267127,1,6.5448257634777e-05,0.442574443496706,0.199060871333091
"ABCF2",0.670677712207237,1.14881588404844,0.65090009812915,1.76496498825307,0.101522292387985,0.581516139764209,3.35737816450296e-05,0.288072975403842,0.0775696501478055
"ABI1",0,0.557009464450956,0.321304309432223,1.73358852682446,0.621327249947296,1,0.000104098172484899,0.297837281912253,0.0829911176161746
```
line count: 1,921

### `tcr_loc_dict*.pickle` (1 file)

inspected: `SCP1348/SCP1348/other/tcr_loc_dict_s1_2020-08-31_Puck_200727_02.pickle` (654.57 KB)

pickle protocol: 5; scanned first 654.57 KB without unpickling
first short strings (attribute names, keys): CASSRANYEQYF, CAASDNYQLIW, CALGDPSNTNKVVF, RASSRATYEQYF, CAT**Q_NAPRF, CAASGNYQLVW, CAASDNCQLVW, CAASGNCQLIW, CAMERGTL_ANTGKLTF, CAAGDNYQLVW, CANNSGGSNAKLTF, CAMREDTGYQNFYF, CALEGFITGNTGKLIF, CASSI_EQYF, CALEQN**_KLAFFFF, CAALNYNQGKLIF, CAASAGRQGTGSKLSF, CARQHG_YKLTF, CAAGGSNAKLTF, CAMRER_YQNFYF, CAMGGGYQNFYF, CAPQHG_YQNFYF, CAASRRDKT_NTGYQNFYF, WGGRQW_SKLSF, CAVNDFQKLVF, CAGLTGKTGKLIF, CAR*RFS_LGRLHF, CALSEREL_NQGKLIF, CAMGGV_QNFYF, CAASRDRINRKLAFFFF, CASRQQDTQYF, CAMREGTGYQNFYL, CASRADYEQYF, CAMRF, CASRK_LRRF
note: loading this needs the original authors' Python classes; treat as untrusted code.

### `trac*.pickle` (1 file)

inspected: `SCP1348/SCP1348/other/trac_trbc2_constant_umis_2020-08-31_Puck_200727_02.pickle` (3.33 MB)

pickle protocol: 4; scanned first 3.33 MB without unpickling
first short strings (attribute names, keys): Trac, AGTAGGGTTTTTTT, TTTTTTTTT, CACAGAAGCTAGCA, GCATTATAG, GAGATGTTAACTAG, ATTTTGTGA, GTTTATCACTCATG, TTTTCAGCA, CCCAGCCCTTTATA, TGAAGCTGA, TACTTGACCCAGAG, GATCTTTTA, ACTCTCGATGAGGA, GGAACGGCG, GCATTAATCACCTC, GGGCCCTCG, GCACACATCAGCCT, TTTGAAAAT, GTTCGCTCACAAAA, GAGAGGACC, TCAGCCATTAGGTG, GGCTTGTCG, TAGAAGGATGAGTT, TGGTGGCAT, CCGCGGTCTGCGAT, ATTATCGCG, CTCCCGCAAAGCTG, TGCTCCGCA, TGTACCTATCTTGT, ACCTATCTT, CAGGAGACTTGACT, GCGCACCAG, CAAGCCTTTTTTTT, TTTCAATTA, AACCATAACGTTCC, CGAGAAATT, ATGGTTGGGGTTAA, ATCCGGCTA, CCTCTCGTATAGCT, TAGTTACCA, AAATTCCTTGTGCC, AGCGTTGGT, TGAAATTAA, AGGAAGTTGCCATA, GTGGGTTAG, AAATTCCTTGTTCC, CAACGTACGCTCAA, CTCGGAGGC, GGCAGTGGTGTTCT, GGGCCGTGG, TTTTCCGGCGTAAT, AGGCACGGG, CGCGCCTTTCACAG, GGAACGTCT, CGCGCCTCTCACAG, GAGACTACTCACTA, GCAAGTGGC, CCATCGTCTCGAGC, GTGAAGTAG
note: loading this needs the original authors' Python classes; treat as untrusted code.

### `tumor_proximity_de_genes.csv` (1 file)

inspected: `SCP1348/SCP1348/other/tumor_proximity_de_genes.csv` (427.45 KB)

delimiter: comma; columns in first line: 10
first lines:
```text
"","tau","log_fc_est","sd_est","Z_est","p_cross","ct_prop","expr","q_val","p"
"A2M",0,-0.238593308293081,0.0949655776160417,-2.51241886041851,0.731927517386089,1,0.00039452919854339,0.250992619741368,0.0119906675379317
"AAMDC",0.16291144824123,-0.247284053521273,0.190995385412028,-1.29471218892444,0.62166283855347,1,3.81086931166809e-05,0.708395809206157,0.195419533574112
"AAMP",0,0.102641633852479,0.141752469042806,0.72409062463303,0.71889423045552,1,0.000133443099916991,0.857043992851215,0.469010099994306
"AATF",0,2.48118674158608e-05,0.16348400673242,0.000151769386570463,0.656119147728341,0.926173521541312,6.06164432523445e-05,0.999878905550118,0.999878905550118
"ABCB4",0.173311851654494,-0.675762336695822,0.256017047960527,-2.63952085253327,0.289672539540301,1,4.96278471925887e-06,0.216015804014616,0.00830233154797555
```
line count: 2,785

## dryad_h70rxwdmj

| kind | n files | total size | example |
|---|---|---|---|
| *.txt | 1 | 136 B | sha256_check_20261101.txt |
| *.zip | 1 | 7.87 GB | 10XVisium_2.zip |
| IMC*.zip | 1 | 1.20 GB | IMC_1.zip |
| MALDI*.zip | 1 | 747.28 MB | MALDI_1.zip |
| Methylation.zip | 1 | 118.83 MB | Methylation.zip |
| PROVENANCE_NOTE.txt | 1 | 126 B | PROVENANCE_NOTE.txt |
| README.md | 1 | 9.55 KB | README.md |
| provenance_failed*.tsv | 1 | 1.43 KB | provenance_failed_401.tsv |
| scSlices_Environment.zip | 1 | 544.50 MB | scSlices_Environment.zip |
| scTumor_Tissue.zip | 1 | 48.74 MB | scTumor_Tissue.zip |

### `*.txt` (1 file)

inspected: `dryad_h70rxwdmj/sha256_check_20261101.txt` (136 B)

delimiter: space; columns in first line: 2
first lines:
```text
10XVisium_2.zip: OK
IMC_1.zip: OK
MALDI_1.zip: OK
Methylation.zip: OK
README.md: OK
scSlices_Environment.zip: OK
```
line count: 7

### `*.zip` (1 file)

inspected: `dryad_h70rxwdmj/10XVisium_2.zip` (7.87 GB)

members: 543 files, 8.44 GB uncompressed
top-level folders (first two levels) and file counts:
```text
    22  10XVisium 2/#UKF248_T_ST
    21  10XVisium 2/#UKF304_T_ST
    21  10XVisium 2/#UKF334_T_ST
    21  10XVisium 2/#UKF243_T_ST
    21  10XVisium 2/#UKF275_T_ST
    20  10XVisium 2/#UKF265_T_ST
    20  10XVisium 2/#UKF248_C_ST
    20  10XVisium 2/#UKF334_C_ST
    20  10XVisium 2/#UKF313_C_ST
    20  10XVisium 2/#UKF296_T_ST
    19  10XVisium 2/#UKF256_TC_ST
    19  10XVisium 2/#UKF260_T_ST
    19  10XVisium 2/#UKF268_IDHMutant_T_ST
    19  10XVisium 2/#UKF256_TI_ST
    19  10XVisium 2/#UKF266_T_ST
    19  10XVisium 2/#UKF241_C_ST
    19  10XVisium 2/#UKF269_T_ST
    19  10XVisium 2/#UKF242_T_ST
    19  10XVisium 2/#UKF262_T_ST
    19  10XVisium 2/#UKF313_T_ST
    18  10XVisium 2/#UKF242_C_ST
    18  10XVisium 2/#UKF270_IDHMutant_T_ST
    18  10XVisium 2/#UKF256_C_ST
    18  10XVisium 2/#UKF251_T_ST
    18  10XVisium 2/#UKF259_C_ST
    18  10XVisium 2/#UKF259_T_ST
    18  10XVisium 2/#UKF255_T_ST
    18  10XVisium 2/#UKF265_C_ST
     3  10XVisium 2
```
first members:
```text
     165 B  10XVisium 2/~$Description.xlsx
  14.34 KB  10XVisium 2/.DS_Store
     783 B  10XVisium 2/README.rtf
   6.15 KB  10XVisium 2/#UKF304_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF256_TC_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF260_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF334_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF268_IDHMutant_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF256_TI_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF266_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF241_C_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF242_C_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF269_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF265_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF248_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF248_C_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF243_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF242_T_ST/.DS_Store
   6.15 KB  10XVisium 2/#UKF262_T_ST/.DS_Store
   8.60 MB  10XVisium 2/#UKF304_T_ST/outs/web_summary.html
     952 B  10XVisium 2/#UKF304_T_ST/outs/metrics_summary.csv
  62.67 MB  10XVisium 2/#UKF304_T_ST/outs/molecule_info.h5
   7.93 MB  10XVisium 2/#UKF304_T_ST/outs/filtered_feature_bc_matrix.h5
   8.37 MB  10XVisium 2/#UKF304_T_ST/outs/raw_feature_bc_matrix.h5
 792.73 MB  10XVisium 2/#UKF304_T_ST/H&E/#UKF_304_RT.tif
   7.58 MB  10XVisium 2/#UKF256_TC_ST/outs/web_summary.html
     943 B  10XVisium 2/#UKF256_TC_ST/outs/metrics_summary.csv
   2.05 MB  10XVisium 2/#UKF256_TC_ST/outs/molecule_info.h5
 480.98 KB  10XVisium 2/#UKF256_TC_ST/outs/filtered_feature_bc_matrix.h5
 576.43 KB  10XVisium 2/#UKF256_TC_ST/outs/raw_feature_bc_matrix.h5
  20.46 MB  10XVisium 2/#UKF256_TC_ST/H&E/#UKF_256_TC.jpeg
   8.65 MB  10XVisium 2/#UKF313_T_ST/outs/web_summary.html
     948 B  10XVisium 2/#UKF313_T_ST/outs/metrics_summary.csv
  63.31 MB  10XVisium 2/#UKF313_T_ST/outs/molecule_info.h5
   7.39 MB  10XVisium 2/#UKF313_T_ST/outs/filtered_feature_bc_matrix.h5
   8.06 MB  10XVisium 2/#UKF313_T_ST/outs/raw_feature_bc_matrix.h5
 562.43 MB  10XVisium 2/#UKF313_T_ST/H&E/#UKF_313_RT.TIF
   5.26 MB  10XVisium 2/#UKF270_IDHMutant_T_ST/outs/web_summary.html
     948 B  10XVisium 2/#UKF270_IDHMutant_T_ST/outs/metrics_summary.csv
  46.24 MB  10XVisium 2/#UKF270_IDHMutant_T_ST/outs/molecule_info.h5
... 503 more
```
head of `10XVisium 2/#UKF304_T_ST/outs/metrics_summary.csv`:
```text
Sample ID,Number of Spots Under Tissue,Median Genes per Spot,Number of Reads,Valid Barcodes,Valid UMIs,Mean Reads per Spot,Sequencing Saturation,Q30 Bases in Barcode,Q30 Bases in RNA Read,Q30 Bases in UMI,Reads Mapped to Genome,Reads Mapped Confidently to Genome,Reads Mapped Confidently to Intergenic Regions,Reads Mapped Confidently to Intronic Regions,Reads Mapped Confidently to Exonic Regions,Re
Sample_304_Recurrent,3123,1766.0,87792484.0,0.9760389739057844,0.9994380954068915,28111.586295228946,0.8147624573519556,0.9801830332652022,0.8683549779865376,0.9764367794429109,0.9324052614800146,0.8786729738732532,0.05796878921890398,0.024329816206134457,0.7963743684482147,0.7598337233515343,0.00921903519668039,0.9742767617260507,20818,3722.0,0.6256009615384616

```
head of `10XVisium 2/#UKF304_T_ST/outs/filtered_feature_bc_matrix/features.tsv.gz`:
```text
ENSG00000243485	MIR1302-2HG	Gene Expression
ENSG00000237613	FAM138A	Gene Expression
ENSG00000186092	OR4F5	Gene Expression
ENSG00000238009	AL627309.1	Gene Expression
ENSG00000239945	AL627309.3	Gene Expression
```
head of `10XVisium 2/#UKF304_T_ST/outs/filtered_feature_bc_matrix/barcodes.tsv.gz`:
```text
AAACAAGTATCTCCCA-1
AAACAGAGCGACTCCT-1
AAACAGGGTCTATATT-1
AAACATTTCCCGGATT-1
AAACCCGAACGAAATC-1
```
head of `10XVisium 2/#UKF304_T_ST/outs/filtered_feature_bc_matrix/matrix.mtx.gz`:
```text
%%MatrixMarket matrix coordinate integer general
%metadata_json: {"software_version": "spaceranger-1.0.0", "format_version": 2}
33538 3123 5309961
33509 1 108
33507 1 20
```
head of `10XVisium 2/#UKF304_T_ST/outs/spatial/Top_GeneExpression_304_T.csv`:
```text
"","barcodes","Radial Glia","Reactive_Immune","Neuronal Developmemnt","OPC","Reactive-Hypoxia"
"1","AAACAAGTATCTCCCA-1",0.45926275370147,0.232449904873765,0.833800111011736,0.408816822492776,0.753927834537485
"2","AAACAGAGCGACTCCT-1",0.70333104639859,0.536085171191975,0.115587999845245,0.645970754539532,0.548103788897794
"3","AAACAGGGTCTATATT-1",0.545242638086257,0.217650263825245,0.300229332176475,0.512775701619483,0.45161989369134
"4","AAACATTTCCCGGATT-1",0.693872329997232,0.220216459967921,0.195141674447603,0.225135730725824,0.412606012523028
```
head of `10XVisium 2/#UKF304_T_ST/outs/spatial/tissue_positions_list.csv`:
```text
ACGCCTGACACGCGCT-1,0,0,0,1657,2342
TACCGATCCAACACTT-1,0,1,1,1827,2441
ATTAAAGCGGACGAGC-1,0,0,2,1656,2539
GATAAGGGACGATTAG-1,0,1,3,1826,2638
GTGCAAATCACCAATA-1,0,0,4,1655,2736
```

### `IMC*.zip` (1 file)

inspected: `dryad_h70rxwdmj/IMC_1.zip` (1.20 GB)

members: 6 files, 3.26 GB uncompressed
top-level folders (first two levels) and file counts:
```text
     4  IMC_1/raw
     2  IMC_1
```
first members:
```text
   8.20 KB  IMC_1/.DS_Store
     586 B  IMC_1/README.rtf
   1.85 GB  IMC_1/raw/GBM_#UKF_262_#UKF_269_#UKF_275.mcd
     803 B  IMC_1/raw/AntobodyPanel.csv
   1.41 GB  IMC_1/raw/GBM_#UKF_248_#UKF_259_#UKF_260.mcd
   1.94 KB  IMC_1/raw/tags.csv
```
head of `IMC_1/raw/AntobodyPanel.csv`:
```text
Metal.tag;Full;ilastik;gene
Ar80;0;0;Ar80
Y89;1;1;CD45
Cd111;1;0;CD4
In113;1;0;VEGFA
```
head of `IMC_1/raw/tags.csv`:
```text
"Tag";"Gene"
"1";"Start_push";"Start_push"
"2";"End_push";"End_push"
"3";"Pushes_duration";"Pushes_duration"
"4";"X";"X"
```

### `MALDI*.zip` (1 file)

inspected: `dryad_h70rxwdmj/MALDI_1.zip` (747.28 MB)

members: 5 files, 1.33 GB uncompressed
top-level folders (first two levels) and file counts:
```text
     3  MALDI_1/raw
     2  MALDI_1
```
first members:
```text
   6.15 KB  MALDI_1/.DS_Store
     583 B  MALDI_1/README.txt.rtf
   1.13 GB  MALDI_1/raw/20201029scilslab_ncfr_glia_combine_root_mean_square.ibd
   6.15 KB  MALDI_1/raw/.DS_Store
 206.15 MB  MALDI_1/raw/20201029scilslab_ncfr_glia_combine_root_mean_square.imzML
```

### `Methylation.zip` (1 file)

inspected: `dryad_h70rxwdmj/Methylation.zip` (118.83 MB)

members: 19 files, 218.86 MB uncompressed
top-level folders (first two levels) and file counts:
```text
    17  Methylation/raw
     2  Methylation
```
first members:
```text
   6.15 KB  Methylation/.DS_Store
     248 B  Methylation/Meta.csv
   6.15 KB  Methylation/raw/.DS_Store
  13.68 MB  Methylation/raw/GS N-13/204900610015_R07C01_Grn.idat
  13.68 MB  Methylation/raw/GS N-13/204900610015_R07C01_Red.idat
  13.68 MB  Methylation/raw/GS N-12/204894630081_R08C01_Grn.idat
  13.68 MB  Methylation/raw/GS N-12/204894630081_R08C01_Red.idat
  13.68 MB  Methylation/raw/GS H-10/204894630081_R05C01_Grn.idat
  13.68 MB  Methylation/raw/GS H-10/204894630081_R05C01_Red.idat
  13.68 MB  Methylation/raw/GS H-11/204894630081_R07C01_Grn.idat
  13.68 MB  Methylation/raw/GS H-11/204894630081_R07C01_Red.idat
  13.68 MB  Methylation/raw/GS N-10/204894630081_R04C01_Red.idat
  13.68 MB  Methylation/raw/GS N-10/204894630081_R04C01_Grn.idat
  13.68 MB  Methylation/raw/GS N-11/204894630081_R06C01_Red.idat
  13.68 MB  Methylation/raw/GS N-11/204894630081_R06C01_Grn.idat
  13.68 MB  Methylation/raw/GS H-13/204900610015_R08C01_Grn.idat
  13.68 MB  Methylation/raw/GS H-13/204900610015_R08C01_Red.idat
  13.68 MB  Methylation/raw/GS H-12/204900610015_R06C01_Red.idat
  13.68 MB  Methylation/raw/GS H-12/204900610015_R06C01_Grn.idat
```
head of `Methylation/Meta.csv`:
```text
file,sample,cond
204894630081_R05C01,GS_10,H
204894630081_R07C01,GS_11,H
204894630081_R04C01,GS_10,N
204894630081_R06C01,GS_11,N
```

### `PROVENANCE_NOTE.txt` (1 file)

inspected: `dryad_h70rxwdmj/PROVENANCE_NOTE.txt` (126 B)

delimiter: space; columns in first line: 13
first lines:
```text
uploaded from F:/Tcellworldmodel/SPTCR-seq/Data on 2026-11-02T02:20:19Z; local sha256 matched Dryad API digests on 2026-11-01

```
line count: 1

### `README.md` (1 file)

inspected: `dryad_h70rxwdmj/README.md` (9.55 KB)

first lines:
```text
# Spatially resolved multi-omics deciphers bidirectional tumor-host interdependence in glioblastoma

#### Author Information

* **Name**: Dr. Vidhya M. Ravi\
  **Institution**: University Clinic of Freiburg\
```
line count: 237

### `provenance_failed*.tsv` (1 file)

inspected: `dryad_h70rxwdmj/provenance_failed_401.tsv` (1.43 KB)

delimiter: tab; columns in first line: 8
first lines:
```text
date_utc	path	url	size_bytes	digest_type	digest_expected	digest_observed	status
2026-11-02T02:03:53Z	10XVisium_2.zip	https://datadryad.org/api/v2/files/3932209/download	7866736112	sha-256	153157e82e9e0df092bb4fcc20dc664ff0dc6643776cb6373e092b6723e1f48a		FAILED(rc=0,size=56)
2026-11-02T02:03:53Z	IMC_1.zip	https://datadryad.org/api/v2/files/3932207/download	1199227587	sha-256	fc40f45904fb5465ea9fd78d1f0e0f25b303ccb3b088fe2b5505dd63cf6f6481		FAILED(rc=0,size=56)
2026-11-02T02:03:53Z	MALDI_1.zip	https://datadryad.org/api/v2/files/3932208/download	747277075	sha-256	f16aace2aa7c61b186bc4a07fc39ebeeb8779f2bd645225985d68e0115aee6df		FAILED(rc=0,size=56)
2026-11-02T02:03:54Z	Methylation.zip	https://datadryad.org/api/v2/files/3932204/download	118834021	sha-256	1590dd7799409c0711cf8f6ff79440a55929cca40f1f479b1ced3eedada3ac16		FAILED(rc=0,size=56)
2026-11-02T02:03:54Z	README.md	https://datadryad.org/api/v2/files/3932212/download	9553	sha-256	165a485d05d46d28e6e95ee22325d623e13f647515397c700e60ee78ed2e9aab		FAILED(rc=0,size=56)
```
line count: 8

### `scSlices_Environment.zip` (1 file)

inspected: `dryad_h70rxwdmj/scSlices_Environment.zip` (544.50 MB)

members: 45 files, 661.77 MB uncompressed
top-level folders (first two levels) and file counts:
```text
    13  scSlices_Environment/#UKF315_SliceTumor
     6  scSlices_Environment/#RAT_3week
     6  scSlices_Environment/#RAT_2y
     6  scSlices_Environment/#UKF316_SliceTumor
     6  scSlices_Environment/#UKF233
     6  scSlices_Environment/#UKF388_SliceTumor
     2  scSlices_Environment
```
first members:
```text
   8.20 KB  scSlices_Environment/.DS_Store
     942 B  scSlices_Environment/README.txt.rtf
   6.15 KB  scSlices_Environment/#RAT_3week/.DS_Store
   6.15 KB  scSlices_Environment/#RAT_2y/.DS_Store
   8.20 KB  scSlices_Environment/#UKF316_SliceTumor/.DS_Store
   6.15 KB  scSlices_Environment/#UKF233/.DS_Store
   6.15 KB  scSlices_Environment/#UKF388_SliceTumor/.DS_Store
   6.15 KB  scSlices_Environment/#UKF315_SliceTumor/.DS_Store
   6.15 KB  scSlices_Environment/#RAT_3week/outs/.DS_Store
   5.42 MB  scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scSlices_Environment/#RAT_2y/outs/.DS_Store
  14.17 MB  scSlices_Environment/#RAT_2y/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scSlices_Environment/#UKF316_SliceTumor/outs/.DS_Store
  10.29 MB  scSlices_Environment/#UKF316_SliceTumor/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scSlices_Environment/#UKF233/outs/.DS_Store
  17.45 MB  scSlices_Environment/#UKF233/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scSlices_Environment/#UKF388_SliceTumor/outs/.DS_Store
  10.00 MB  scSlices_Environment/#UKF388_SliceTumor/outs/filtered_feature_bc_matrix.h5
   2.21 MB  scSlices_Environment/#UKF315_SliceTumor/outs/web_summary.html
     683 B  scSlices_Environment/#UKF315_SliceTumor/outs/metrics_summary.csv
 182.33 MB  scSlices_Environment/#UKF315_SliceTumor/outs/molecule_info.h5
   6.15 KB  scSlices_Environment/#UKF315_SliceTumor/outs/.DS_Store
  13.31 MB  scSlices_Environment/#UKF315_SliceTumor/outs/filtered_feature_bc_matrix.h5
 148.41 MB  scSlices_Environment/#UKF315_SliceTumor/outs/raw_feature_bc_matrix.h5
 304.73 KB  scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix/features.tsv.gz
   8.91 KB  scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  13.32 MB  scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scSlices_Environment/#RAT_2y/outs/filtered_feature_bc_matrix/features.tsv.gz
  13.35 KB  scSlices_Environment/#RAT_2y/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  38.02 MB  scSlices_Environment/#RAT_2y/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scSlices_Environment/#UKF316_SliceTumor/outs/filtered_feature_bc_matrix/features.tsv.gz
  10.29 KB  scSlices_Environment/#UKF316_SliceTumor/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  23.06 MB  scSlices_Environment/#UKF316_SliceTumor/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scSlices_Environment/#UKF233/outs/filtered_feature_bc_matrix/features.tsv.gz
  21.65 KB  scSlices_Environment/#UKF233/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  45.87 MB  scSlices_Environment/#UKF233/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scSlices_Environment/#UKF388_SliceTumor/outs/filtered_feature_bc_matrix/features.tsv.gz
   9.96 KB  scSlices_Environment/#UKF388_SliceTumor/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  25.97 MB  scSlices_Environment/#UKF388_SliceTumor/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scSlices_Environment/#UKF315_SliceTumor/outs/filtered_feature_bc_matrix/features.tsv.gz
... 5 more
```
head of `scSlices_Environment/#UKF315_SliceTumor/outs/metrics_summary.csv`:
```text
Estimated Number of Cells,Mean Reads per Cell,Median Genes per Cell,Number of Reads,Valid Barcodes,Sequencing Saturation,Q30 Bases in Barcode,Q30 Bases in RNA Read,Q30 Bases in Sample Index,Q30 Bases in UMI,Reads Mapped to Genome,Reads Mapped Confidently to Genome,Reads Mapped Confidently to Intergenic Regions,Reads Mapped Confidently to Intronic Regions,Reads Mapped Confidently to Exonic Regions,
"4,126","43,193","1,030","178,215,215",97.2%,60.0%,96.4%,92.5%,96.3%,94.9%,88.7%,83.6%,4.3%,27.1%,52.2%,46.9%,3.6%,79.2%,"22,905","2,181"

```
head of `scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix/features.tsv.gz`:
```text
ENSG00000243485	MIR1302-2HG	Gene Expression
ENSG00000237613	FAM138A	Gene Expression
ENSG00000186092	OR4F5	Gene Expression
ENSG00000238009	AL627309.1	Gene Expression
ENSG00000239945	AL627309.3	Gene Expression
```
head of `scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix/barcodes.tsv.gz`:
```text
AAACCCAAGGTGATAT-1
AAACCCATCCAGCCTT-1
AAACGAATCAGTCCGG-1
AAACGCTCATGACGAG-1
AAACGCTTCAGGTGTT-1
```
head of `scSlices_Environment/#RAT_3week/outs/filtered_feature_bc_matrix/matrix.mtx.gz`:
```text
%%MatrixMarket matrix coordinate integer general
%metadata_json: {"software_version": "cellranger-5.0.1", "format_version": 2}
33538 1572 3507531
28 1 1
67 1 1
```

### `scTumor_Tissue.zip` (1 file)

inspected: `dryad_h70rxwdmj/scTumor_Tissue.zip` (48.74 MB)

members: 32 files, 52.05 MB uncompressed
top-level folders (first two levels) and file counts:
```text
     7  scTumor_Tissue/#UKF313_T_SCRNA
     6  scTumor_Tissue/#UKF315_T_SCRNA
     6  scTumor_Tissue/#UKF410_T_SCRNA
     6  scTumor_Tissue/#UKF334_T_SCRNA
     6  scTumor_Tissue/#UKF357_T_SCRNA
     1  scTumor_Tissue
```
first members:
```text
   8.20 KB  scTumor_Tissue/.DS_Store
   6.15 KB  scTumor_Tissue/#UKF315_T_SCRNA/.DS_Store
   6.15 KB  scTumor_Tissue/#UKF410_T_SCRNA/.DS_Store
   6.15 KB  scTumor_Tissue/#UKF334_T_SCRNA/.DS_Store
   6.15 KB  scTumor_Tissue/#UKF357_T_SCRNA/.DS_Store
   6.15 KB  scTumor_Tissue/#UKF313_T_SCRNA/.DS_Store
   6.15 KB  scTumor_Tissue/#UKF315_T_SCRNA/outs/.DS_Store
   6.07 MB  scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scTumor_Tissue/#UKF410_T_SCRNA/outs/.DS_Store
   1.67 MB  scTumor_Tissue/#UKF410_T_SCRNA/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scTumor_Tissue/#UKF334_T_SCRNA/outs/.DS_Store
   6.12 MB  scTumor_Tissue/#UKF334_T_SCRNA/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scTumor_Tissue/#UKF357_T_SCRNA/outs/.DS_Store
   2.67 MB  scTumor_Tissue/#UKF357_T_SCRNA/outs/filtered_feature_bc_matrix.h5
   6.15 KB  scTumor_Tissue/#UKF313_T_SCRNA/outs/.DS_Store
 925.24 KB  scTumor_Tissue/#UKF313_T_SCRNA/outs/filtered_feature_bc_matrix.h5
 304.73 KB  scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix/features.tsv.gz
   8.96 KB  scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  11.01 MB  scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scTumor_Tissue/#UKF410_T_SCRNA/outs/filtered_feature_bc_matrix/features.tsv.gz
   2.20 KB  scTumor_Tissue/#UKF410_T_SCRNA/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
   3.42 MB  scTumor_Tissue/#UKF410_T_SCRNA/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scTumor_Tissue/#UKF334_T_SCRNA/outs/filtered_feature_bc_matrix/features.tsv.gz
   8.79 KB  scTumor_Tissue/#UKF334_T_SCRNA/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
  11.08 MB  scTumor_Tissue/#UKF334_T_SCRNA/outs/filtered_feature_bc_matrix/matrix.mtx.gz
 304.73 KB  scTumor_Tissue/#UKF357_T_SCRNA/outs/filtered_feature_bc_matrix/features.tsv.gz
   3.58 KB  scTumor_Tissue/#UKF357_T_SCRNA/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
   6.01 MB  scTumor_Tissue/#UKF357_T_SCRNA/outs/filtered_feature_bc_matrix/matrix.mtx.gz
  22.08 KB  scTumor_Tissue/#UKF313_T_SCRNA/outs/filtered_feature_bc_matrix/.Rhistory
 304.73 KB  scTumor_Tissue/#UKF313_T_SCRNA/outs/filtered_feature_bc_matrix/features.tsv.gz
   4.97 KB  scTumor_Tissue/#UKF313_T_SCRNA/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
   1.44 MB  scTumor_Tissue/#UKF313_T_SCRNA/outs/filtered_feature_bc_matrix/matrix.mtx.gz
```
head of `scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix/features.tsv.gz`:
```text
ENSG00000243485	MIR1302-2HG	Gene Expression
ENSG00000237613	FAM138A	Gene Expression
ENSG00000186092	OR4F5	Gene Expression
ENSG00000238009	AL627309.1	Gene Expression
ENSG00000239945	AL627309.3	Gene Expression
```
head of `scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix/barcodes.tsv.gz`:
```text
AAACCCATCATGGAGG-1
AAACGAACAAGAGTGC-1
AAACGCTAGGGTCTTT-1
AAAGAACAGGATACCG-1
AAAGAACCAACCGACC-1
```
head of `scTumor_Tissue/#UKF315_T_SCRNA/outs/filtered_feature_bc_matrix/matrix.mtx.gz`:
```text
%%MatrixMarket matrix coordinate integer general
%metadata_json: {"format_version": 2, "software_version": "3.1.0"}
33538 1580 2916668
33509 1 20
33508 1 1
```

## osf_65y3t

| kind | n files | total size | example |
|---|---|---|---|
| *T_ST_Exhausted_NCEM_Object_type_coupling.csv | 3 | 142.44 KB | #UKF259_T_ST_Exhausted_NCEM_Object_type_coupling.csv |
| *T_ST_Reactive_NCEM_Object_type_coupling.csv | 7 | 331.71 KB | #UKF260_T_ST_Reactive_NCEM_Object_type_coupling.csv |
| CORRECTED_UMI_CORR_MERGE.csv | 1 | 129.07 MB | CORRECTED_UMI_CORR_MERGE.csv |
| Error_Rate_Plotting.csv | 1 | 188.88 MB | Error_Rate_Plotting.csv |
| Processed_SPTCR_seq.rds | 1 | 15.10 MB | Processed_SPTCR_seq.rds |
| Processed_SPTCR_seq_Histology.rds | 1 | 356.50 KB | Processed_SPTCR_seq_Histology.rds |
| Raw_SPTCR_seq.rds | 1 | 120 B | Raw_SPTCR_seq.rds |
| UNCORRECTED_UMI_CORR_MERGE.csv | 1 | 272.22 MB | UNCORRECTED_UMI_CORR_MERGE.csv |
| nn_clonal.rds | 1 | 35.95 KB | nn_clonal.rds |
| nn_diverse.rds | 1 | 35.95 KB | nn_diverse.rds |
| plotting_stacked_bar.csv | 1 | 528.96 MB | plotting_stacked_bar.csv |
| provenance.tsv | 1 | 5.75 KB | provenance.tsv |

### `*T_ST_Exhausted_NCEM_Object_type_coupling.csv` (3 files)

inspected: `osf_65y3t/NCEM/#UKF259_T_ST_Exhausted_NCEM_Object_type_coupling.csv` (46.14 KB)

delimiter: comma; columns in first line: 7
first lines:
```text
,sender,receiver,0,magnitude,de_genes,de_genes_abs
1,Ac-Like,B Cell,26,3.166527536521655,0.09454545454545454,26
2,Ac-Like,Cd4 Inf,25,2.9919980275913116,0.09090909090909091,25
3,Ac-Like,Cd8 Cytotoxic,25,6.612732764547781,0.09090909090909091,25
4,Ac-Like,Cd8 Nk Sig,30,1.3547542272385538,0.10909090909090909,30
5,Ac-Like,Cdc1,20,1.4431856065076178,0.07272727272727272,20
```
line count: 703

### `*T_ST_Reactive_NCEM_Object_type_coupling.csv` (7 files)

inspected: `osf_65y3t/NCEM/#UKF260_T_ST_Reactive_NCEM_Object_type_coupling.csv` (39.56 KB)

delimiter: comma; columns in first line: 7
first lines:
```text
,sender,receiver,0,magnitude,de_genes,de_genes_abs
1,Ac-Like,B Cell,18,1.6696509688752366,0.045,18
2,Ac-Like,Cd4 Inf,11,0.5548868939525269,0.0275,11
3,Ac-Like,Cd8 Cytotoxic,7,0.42544478638417477,0.0175,7
4,Ac-Like,Cd8 Nk Sig,22,1.04915019440563,0.055,22
5,Ac-Like,Cdc1,17,0.7867535384897071,0.0425,17
```
line count: 703

### `CORRECTED_UMI_CORR_MERGE.csv` (1 file)

inspected: `osf_65y3t/Figure 1c and 2a_b/CORRECTED_UMI_CORR_MERGE.csv` (129.07 MB)

delimiter: comma; columns in first line: 8
first lines:
```text
Spatial Barcode,Uncorrected Count,UMI Corrected,Locus,V,D,J,CDR3_aa
CGACCCGCTTGAATCT,6206,77,TRB,TRBV21-1*01,TRBD1*01,TRBJ1-3*01,ASSMVELDRGMETPY
AGATTCAAGCGGGTCG,5388,72,TRB,TRBV21-1*01,TRBD1*01,TRBJ1-3*01,ASSMVELDRGMETPY
TGTCTACCCAAAGCCA,4069,46,TRB,TRBV28*01,TRBD2*02,TRBJ2-1*01,ASSSERGSSYNEQF
ACACTTAGGGATGCGA,4057,41,TRB,TRBV25-1*01,TRBD2*02,TRBJ2-3*01,ASSEAGGPDTQY
CCGTACTCAGACCGGT,3831,77,TRB,TRBV12-2*01,TRBD1*01,TRBJ2-3*01,KRVPTRGRCV*AIRSRDLPHPKGHTGVPGHRLLPRPRGAELVGEWEGGAQWGQHRPA
```
line count: 1,774,468

### `Error_Rate_Plotting.csv` (1 file)

inspected: `osf_65y3t/Figure 2d and e/Error_Rate_Plotting.csv` (188.88 MB)

delimiter: comma; columns in first line: 3
first lines:
```text
acc,Corrected,Uncorrected
27:763|7337da9c-9707-4a5c-be35-c3e597d3df4d,0.0,8.2143
27:764|12525e59-f672-474d-b7d9-3e4dc9a778e9,0.0,2.5547
25:704|6c0dd3f9-759b-455e-bede-e6b9ed3f51c5,0.0,1.7391
30:663|b15c2d73-317d-4965-9d98-c352fb194591,0.0,0.0
31:661|4ac9a5f9-4b26-40cc-a57b-fb621d11dbad,0.0,4.698
```
line count: 3,278,865

### `Processed_SPTCR_seq.rds` (1 file)

inspected: `osf_65y3t/Processed_SPTCR_seq.rds` (15.10 MB)

R serialized object (readRDS): compression=gzip, format=XDR binary; open with R to see the class

### `Processed_SPTCR_seq_Histology.rds` (1 file)

inspected: `osf_65y3t/Processed_SPTCR_seq_Histology.rds` (356.50 KB)

R serialized object (readRDS): compression=gzip, format=XDR binary; open with R to see the class

### `Raw_SPTCR_seq.rds` (1 file)

inspected: `osf_65y3t/Raw_SPTCR_seq.rds` (120 B)

R serialized object (readRDS): compression=gzip, format=XDR binary; open with R to see the class

### `UNCORRECTED_UMI_CORR_MERGE.csv` (1 file)

inspected: `osf_65y3t/Figure 1c and 2a_b/UNCORRECTED_UMI_CORR_MERGE.csv` (272.22 MB)

delimiter: comma; columns in first line: 8
first lines:
```text
Spatial Barcode,Uncorrected Count,UMI Corrected,Locus,V,D,J,CDR3_aa
ATAGCGCGACTAGTGC,1795,45,TRB,TRBV7-2*01,TRBD1*01,TRBJ1-1*01,ASSFLDRGTEAF
ATAGCGCGACTAGTGC,1717,44,TRB,TRBV7-2*01,TRBD1*01,TRBJ1-1*01,QQLPGQGH*SF
ATAGCGCGACTAGTGC,1703,35,TRB,TRBV7-2*01,TRBD1*01,TRBJ1-1*01,PAASWTGALKLS
CAAACTCTCAAGAGCA,1271,33,TRB,TRBV7-3*01,TRBD1*01,TRBJ1-1*01,QQLNPCPTAEH*SF
CAAACTCTCAAGAGCA,1251,47,TRB,TRBV7-3*01,TRBD1*01,TRBJ1-1*01,PAA*PLSDSRTLKLS
```
line count: 3,747,698

### `nn_clonal.rds` (1 file)

inspected: `osf_65y3t/nn_clonal.rds` (35.95 KB)

R serialized object (readRDS): compression=gzip, format=XDR binary; open with R to see the class

### `nn_diverse.rds` (1 file)

inspected: `osf_65y3t/nn_diverse.rds` (35.95 KB)

R serialized object (readRDS): compression=gzip, format=XDR binary; open with R to see the class

### `plotting_stacked_bar.csv` (1 file)

inspected: `osf_65y3t/Figure 2d and e/plotting_stacked_bar.csv` (528.96 MB)

delimiter: comma; columns in first line: 4
first lines:
```text
,TCR,Count,Correction
0,TRA_TRAV36/DV7*05_TRAJ41*01_GCTGTGGAGGCACAGTGCTCCCTAGTCACCTGCAGCCTGTACTCAAATTC,56857,Corrected
1,TRA_TRAV4*01_TRAJ28*01_CTCGTGGGTGACACACAGTGAGACAGATGGGCCTGCACCTGTGCCGTTTTCCTCTGTGGGGTGGGAGT,6929,Corrected
2,TRA_TRAV38-2/DV8*01_TRAJ44*01_GCTTATAGGACCCTCTGGGGCGGCACTGCCAGTAAACTCACC,6919,Corrected
3,TRA_TRAV30*01_TRAJ13*01_GGCACAGAGAGTTCTGGGGGTTACCAGAAAGTTACC,6097,Corrected
4,TRA_TRAV35*01_TRAJ21*01_GCTGGGGTCCAATACAACTTCAACAAATTTTAC,5654,Corrected
```

### `provenance.tsv` (1 file)

inspected: `osf_65y3t/provenance.tsv` (5.75 KB)

delimiter: tab; columns in first line: 7
first lines:
```text
date_utc	path	url	size_bytes	sha256_expected	sha256_observed	status
2026-11-02T02:08:13Z	nn_diverse.rds	https://osf.io/download/h3znp/?view_only=6571f0c374ce4bf294b9cbd10ade62cf	35947	247f080c6a04e6aef7488cd5021efa47a6fe7a74fb9399c8408c3fb84ebd9620	247f080c6a04e6aef7488cd5021efa47a6fe7a74fb9399c8408c3fb84ebd9620	downloaded
2026-11-02T02:08:16Z	nn_clonal.rds	https://osf.io/download/rt74b/?view_only=6571f0c374ce4bf294b9cbd10ade62cf	35947	247f080c6a04e6aef7488cd5021efa47a6fe7a74fb9399c8408c3fb84ebd9620	247f080c6a04e6aef7488cd5021efa47a6fe7a74fb9399c8408c3fb84ebd9620	downloaded
2026-11-02T02:08:18Z	Processed_SPTCR_seq_Histology.rds	https://osf.io/download/entzv/?view_only=6571f0c374ce4bf294b9cbd10ade62cf	356505	ec299d5c04f631a8764fc61878a02d2f4e6a40b7ca4970f69f7a6438887648ef	ec299d5c04f631a8764fc61878a02d2f4e6a40b7ca4970f69f7a6438887648ef	downloaded
2026-11-02T02:08:23Z	Processed_SPTCR_seq.rds	https://osf.io/download/bwn3h/?view_only=6571f0c374ce4bf294b9cbd10ade62cf	15097305	f3dddd145a47cb8910b4b5a19bf01f69a28875ebb2688b97ceb77e660b26807d	f3dddd145a47cb8910b4b5a19bf01f69a28875ebb2688b97ceb77e660b26807d	downloaded
2026-11-02T02:08:26Z	Raw_SPTCR_seq.rds	https://osf.io/download/8rs49/?view_only=6571f0c374ce4bf294b9cbd10ade62cf	120	d1cc32ec45cc95dc3d8b79e138d5486cbed40adc777446bdccda310bad3e0a4b	d1cc32ec45cc95dc3d8b79e138d5486cbed40adc777446bdccda310bad3e0a4b	downloaded
```
line count: 20

## osf_8qbdz

| kind | n files | total size | example |
|---|---|---|---|
| Integrated_ST_MALDI*T.rds | 6 | 2.95 GB | Integrated_ST_MALDI_262_T.RDS |
| Meta_Use.pdf | 1 | 24.94 MB | Meta_Use.pdf |
| provenance.tsv | 1 | 1.98 KB | provenance.tsv |

### `Integrated_ST_MALDI*T.rds` (6 files)

inspected: `osf_8qbdz/Integrated_ST_MALDI_262_T.RDS` (406.49 MB)

R serialized object (readRDS): compression=gzip, format=XDR binary; open with R to see the class

### `Meta_Use.pdf` (1 file)

inspected: `osf_8qbdz/Meta_Use.pdf` (24.94 MB)

binary: PDF

### `provenance.tsv` (1 file)

inspected: `osf_8qbdz/provenance.tsv` (1.98 KB)

delimiter: tab; columns in first line: 7
first lines:
```text
date_utc	path	url	size_bytes	sha256_expected	sha256_observed	status
2026-11-02T02:04:45Z	Integrated_ST_MALDI_259_T.RDS	https://osf.io/download/6vwdk/?view_only=5287d7f6263e4ba680ca8c396aeefeee	559028742	0de78874906301ec9bb26a300146bc2300759028e5cfe883f6d5bec5d7c84248	0de78874906301ec9bb26a300146bc2300759028e5cfe883f6d5bec5d7c84248	downloaded
2026-11-02T02:05:19Z	Integrated_ST_MALDI_275_T.RDS	https://osf.io/download/dksym/?view_only=5287d7f6263e4ba680ca8c396aeefeee	576754753	25566ce0022661c6dfa8d43a89f52a61852d973f7df5ee831519472b5e80454b	25566ce0022661c6dfa8d43a89f52a61852d973f7df5ee831519472b5e80454b	downloaded
2026-11-02T02:05:45Z	Integrated_ST_MALDI_262_T.RDS	https://osf.io/download/2krjs/?view_only=5287d7f6263e4ba680ca8c396aeefeee	406493920	3fa9ea0a1ebf0ec9f5150d2c98ede30dfd26d8b11c66fa3c165e963d0db7dfca	3fa9ea0a1ebf0ec9f5150d2c98ede30dfd26d8b11c66fa3c165e963d0db7dfca	downloaded
2026-11-02T02:06:17Z	Integrated_ST_MALDI_269_T.RDS	https://osf.io/download/7ep8w/?view_only=5287d7f6263e4ba680ca8c396aeefeee	514402037	6733c74d848f83d0021383d204121dca3aa932da3ba59f94ac3658ea5a27fbde	6733c74d848f83d0021383d204121dca3aa932da3ba59f94ac3658ea5a27fbde	downloaded
2026-11-02T02:06:47Z	Integrated_ST_MALDI_260_T.RDS	https://osf.io/download/mey3p/?view_only=5287d7f6263e4ba680ca8c396aeefeee	446952311	2946a1e3612138c18f68d1c8fb51d4a8f66e7a5a7adb754dbfddd60b413cdabe	2946a1e3612138c18f68d1c8fb51d4a8f66e7a5a7adb754dbfddd60b413cdabe	downloaded
```
line count: 8

## GEO series and sample metadata

Taken from the GEO SOFT records cached during download. Sample characteristics are the authors' own fields; they are the basis for linking samples to patients.

### GSE179572: Spatial transcriptomics of human brain metastases

- **type**: Expression profiling by high throughput sequencing
- **summary**: Spatial transcriptomics of six surgically-resected human brain metastasis samples
- **overall_design**: After surgical resection, parts of six human brain metastases were embedded in OCT and frozen in a dry ice/2-methylbutane bath. 10 μM sections were placed on Visium gene expression slides which were stored at -80C until use. Slides were methanol fixed and stained with H&E and imaged at 10X on a Biotek Lionheart microscope. Tissues were permeabilized and libraries generated according to the manufacturer's protocols. Images for all samples are available in all_spatial_images.tar.gz.
- relation: BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA744217
- relation: SRA: https://www.ncbi.nlm.nih.gov/sra?term=SRP327191

| GSM | title | source | characteristics | library | n supp files |
|---|---|---|---|---|---|
| GSM5420749 | Spatial transcriptomics of a human brain metastasis (pati... | tumor | primary tumor: lung adenocarcinoma; visium gene expressio... | RNA-Seq | 5 |
| GSM5420750 | Spatial transcriptomics of a human brain metastasis (pati... | tumor | primary tumor: melanoma; visium gene expression slideseri... | RNA-Seq | 5 |
| GSM5420751 | Spatial transcriptomics of a human brain metastasis (pati... | tumor | primary tumor: lung adenocarcinoma; visium gene expressio... | RNA-Seq | 5 |
| GSM5420752 | Spatial transcriptomics of a human brain metastasis (pati... | tumor | primary tumor: renal cell carcinoma (clear cell); visium ... | RNA-Seq | 5 |
| GSM5420753 | Spatial transcriptomics of a human brain metastasis (pati... | tumor | primary tumor: breast carcinoma; visium gene expression s... | RNA-Seq | 5 |
| GSM5420754 | Spatial transcriptomics of a human brain metastasis (pati... | tumor | primary tumor: lung adenocarcinoma; visium gene expressio... | RNA-Seq | 5 |

### GSE238071: High-sensitive spatially resolved T cell receptor sequencing with SPTCR-seq

- **type**: Other
- **summary**: Understanding the spatial distribution of T cells is pivotal to decrypting immune dysfunction in cancer. Current spatially resolved transcriptomics fall short in directly annotating T cell receptors (TCRs), limiting the comprehension of anti-cancer immunity. We introduce a novel technology, Spatially Resolved T Cell Receptor Sequencing (SPTCR-seq), integrating target enrichment and long-read sequencing for highly sensitive TCR sequencing. This approach yields an on-target rate of ~85%, and via a bespoke computational pipeline, it provides meticulous spatial mapping, error correction, and UMI refinement. SPTCR-seq outperforms PCR-based methods, offering superior reconstruction of the complete TCR architecture, inclusive of V, D, J regions and the vital complementarity-determining region 3 (CDR3). Applying SPTCR-seq, we reveal local T cell diversity, clonal expansion, and transcriptiona...
- **overall_design**: The Spatial Transcriptomics-based T Cell Receptor sequencing (SPTCR) approach begins by generating full-length cDNA from fresh frozen glioblastoma tissue samples. This cDNA is enriched for T cell receptor (TCR) sequences using custom probes, then undergoes long-read nanopore sequencing for a thorough interpretation of TCR diversity. Following sequencing, computational processing is employed for TCR annotation, error correction, and clonality analysis. SPTCR combines this information with spatial transcriptomics data, mapping TCR sequences to their original spatial context within the tumor. Finally, integration with imaging mass spectrometry metabolomics data allows for a unique exploration of TCR clonal expansion, exhaustion, and metabolism within the tumor microenvironment. The spatial transcriptomics data related to this study has been deposited on DataDryad and is accessible to the...
- relation: BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA997917

| GSM | title | source | characteristics | library | n supp files |
|---|---|---|---|---|---|
| GSM7658219 | UKF248_T_SPTCR15 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: m; ... | OTHER | 1 |
| GSM7658220 | UKF259_T_SPTCR12 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: f; ... | OTHER | 1 |
| GSM7658221 | UKF260_T_SPTCR13 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: m; ... | OTHER | 1 |
| GSM7658222 | UKF269_T_SPTCR2 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: m; ... | OTHER | 1 |
| GSM7658223 | UKF275_T_SPTCR16 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: f; ... | OTHER | 1 |
| GSM7658224 | UKF296_T_SPTCR20 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: m; ... | OTHER | 1 |
| GSM7658225 | UKF304_T_SPTCR17 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: m; ... | OTHER | 1 |
| GSM7658226 | UKF313_T_SPTCR9 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: m; ... | OTHER | 1 |
| GSM7658227 | UKF334_T_SPTCR14 | Brain Tumor | disease state: Glioblastoma; idh-status: IDH-WT; Sex: f; ... | OTHER | 1 |

### GSE285951: T cell receptor sequencing of HNSCC patient and healthy donor peripheral blood

- **type**: Other
- **summary**: This dataset comprises TCR-seq data from peripheral blood CD4+ and CD8+ T cells of head and neck squamous cell carcinoma (HNSCC) patients and healthy donors. Viable peripheral blood mononuclear cells (PBMCs) were sorted into CD45+CD3+CD4+ (CD4+ T cells) and CD45+CD3+CD8+ (CD8+ T cells) subsets, and RNA was isolated using the Qiagen AllPrep DNA/RNA Micro kit. TCR libraries were prepared with the SMART-Seq Human TCR-seq with UMIs kit (Takara Bio) and sequenced on an Illumina NovaSeq X Plus platform. This dataset includes samples from 27 tumor patients and five healthy donors (HDs).  The study aims to investigate the phenotype, function, and spatial localization of T cells in HNSCC patients. This peripheral blood dataset focuses on characterizing circulating immune determinants of anti-HNSCC immunity and linking circulating T cell clones to those identified in patient-matched tumor scRNA...
- **overall_design**: CD4+ and CD8+ T cells were sorted from PBMCs of 27 HNSCC patients and 5 healthy donors (HDs). RNA was isolated and TCRs were sequenced using the SMART-Seq Human TCR-seq with UMIs kit from Takara Bio.
- relation: BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1207033

| GSM | title | source | characteristics | library | n supp files |
|---|---|---|---|---|---|
| GSM8713798 | TCR sequences of CD8 T cells from patient 15 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713799 | TCR sequences of CD8 T cells from patient 4 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713800 | TCR sequences of CD8 T cells from patient 6 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713801 | TCR sequences of CD8 T cells from patient 26 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713802 | TCR sequences of CD8 T cells from patient 27 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713803 | TCR sequences of CD8 T cells from patient 20 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713804 | TCR sequences of CD4 T cells from patient 20 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713805 | TCR sequences of CD8 T cells from patient 11 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713806 | TCR sequences of CD4 T cells from patient 15 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713807 | TCR sequences of CD8 T cells from patient 28 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713808 | TCR sequences of CD8 T cells from patient 17 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713809 | TCR sequences of CD8 T cells from patient 1 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713810 | TCR sequences of CD8 T cells from patient 10 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713811 | TCR sequences of CD8 T cells from patient 19 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713812 | TCR sequences of CD8 T cells from patient 8 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713813 | TCR sequences of CD8 T cells from patient 7 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713814 | TCR sequences of CD4 T cells from patient 28 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713815 | TCR sequences of CD8 T cells from patient HD1 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713816 | TCR sequences of CD8 T cells from patient 2 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713817 | TCR sequences of CD8 T cells from patient 16 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713818 | TCR sequences of CD4 T cells from patient 27 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713819 | TCR sequences of CD8 T cells from patient 5 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713820 | TCR sequences of CD4 T cells from patient 6 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713821 | TCR sequences of CD8 T cells from patient HD3 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713822 | TCR sequences of CD8 T cells from patient 3 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713823 | TCR sequences of CD8 T cells from patient 12 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713824 | TCR sequences of CD8 T cells from patient 9 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713825 | TCR sequences of CD4 T cells from patient 9 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713826 | TCR sequences of CD4 T cells from patient 22 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713827 | TCR sequences of CD4 T cells from patient 13 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713828 | TCR sequences of CD4 T cells from patient 3 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713829 | TCR sequences of CD8 T cells from patient 22 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713830 | TCR sequences of CD8 T cells from patient 23 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713831 | TCR sequences of CD8 T cells from patient HD2 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713832 | TCR sequences of CD4 T cells from patient 18 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713833 | TCR sequences of CD4 T cells from patient HD1 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713834 | TCR sequences of CD4 T cells from patient 19 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713835 | TCR sequences of CD8 T cells from patient 18 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713836 | TCR sequences of CD4 T cells from patient 5 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713837 | TCR sequences of CD4 T cells from patient HD2 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713838 | TCR sequences of CD4 T cells from patient 23 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713839 | TCR sequences of CD8 T cells from patient 13 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713840 | TCR sequences of CD4 T cells from patient 1 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713841 | TCR sequences of CD4 T cells from patient 2 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713842 | TCR sequences of CD4 T cells from patient 12 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713843 | TCR sequences of CD4 T cells from patient 4 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713844 | TCR sequences of CD8 T cells from patient HD4 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713845 | TCR sequences of CD4 T cells from patient 7 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713846 | TCR sequences of CD4 T cells from patient 25 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713847 | TCR sequences of CD8 T cells from patient 14 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |
| GSM8713848 | TCR sequences of CD4 T cells from patient 16 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713849 | TCR sequences of CD4 T cells from patient 10 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713850 | TCR sequences of CD4 T cells from patient HD3 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713851 | TCR sequences of CD4 T cells from patient HD4 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713852 | TCR sequences of CD4 T cells from patient 11 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713853 | TCR sequences of CD4 T cells from patient 21 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713854 | TCR sequences of CD4 T cells from patient 14 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713855 | TCR sequences of CD4 T cells from patient 17 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713856 | TCR sequences of CD4 T cells from patient HD5 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713857 | TCR sequences of CD4 T cells from patient 26 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713858 | TCR sequences of CD4 T cells from patient 8 | PBMCs | tissue: PBMCs; cell type: CD4 T cells | OTHER | 1 |
| GSM8713859 | TCR sequences of CD8 T cells from patient HD5 | PBMCs | tissue: PBMCs; cell type: CD8 T cells | OTHER | 1 |

### GSE287301: Single-cell RNA-sequencing of HNSCC-infiltrating T cells

- **type**: Expression profiling by high throughput sequencing
- **summary**: This study examines the T cell landscape in head and neck squamous cell carcinoma (HNSCC) using single-cell RNA sequencing combined with T cell receptor and protein profiling. By analyzing tumor-infiltrating T cells from 28 patients, we identified diverse T cell subsets, characterized their transcriptional states, and mapped their clonal dynamics. These findings provide a detailed view of the immune microenvironment in HNSCC and offer insights into T cell-mediated immunity and potential targets for immunotherapy and are patient-matched to PBMC TCR sequencing and Xenium spatial transcriptomics in separate GEO submissions.
- **overall_design**: T cells (CD45+CD3+) were sorted from 28 patients with head and neck and squamous cell carcinoma (HNSCC) using a Cytek Aurora Cell Sorter. Cells originating from each patient were labeled with one Totalseq-C human hashtag antibody (BioLegend). Four patient samples with distinct hashtags were pooled and loaded into one well of a GEM-X microfluidics chip (10x Genomics). 16 GEM-X reactions were performed, run on two independent GEM-X microfluidics chips. Pools 1-7 were replicated on both chips, and two pools (pool 8 and pool 16) were each run on one chip. Hashes used for each patient and the patient composition of each pool are described in the patient_matrix.txt supplementary file. Hashtag sequences are as follows:  Hashing antibody sequences: hashtag 1 - GTCAACTCTTTAGCG; hashtag 2 - TGATGGCCTATTGGG; hashtag 3 - TTCCGCCTCTCTTTG; hashtag 4 - AGTAAGTTCAGCGTA.  Gene expression (GEX), T cell...
- relation: BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1212073

| GSM | title | source | characteristics | library | n supp files |
|---|---|---|---|---|---|
| GSM8743442 | Gene expression: chip 1 pool 1 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743443 | Gene expression: chip 1 pool 2 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743444 | Gene expression: chip 1 pool 3 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743445 | Gene expression: chip 1 pool 4 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743446 | Gene expression: chip 1 pool 5 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743447 | Gene expression: chip 1 pool 6 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743448 | Gene expression: chip 1 pool 7 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743449 | Gene expression: chip 1 pool 8 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743450 | Gene expression: chip 2 pool 1 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743451 | Gene expression: chip 2 pool 2 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743452 | Gene expression: chip 2 pool 3 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743453 | Gene expression: chip 2 pool 4 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743454 | Gene expression: chip 2 pool 5 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743455 | Gene expression: chip 2 pool 6 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743456 | Gene expression: chip 2 pool 7 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743457 | Gene expression: chip 2 pool 16 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743458 | CITE-seq: chip 1 pool 1 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743459 | CITE-seq: chip 1 pool 2 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743460 | CITE-seq: chip 1 pool 3 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743461 | CITE-seq: chip 1 pool 4 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743462 | CITE-seq: chip 1 pool 5 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743463 | CITE-seq: chip 1 pool 6 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743464 | CITE-seq: chip 1 pool 7 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743465 | CITE-seq: chip 1 pool 8 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743466 | CITE-seq: chip 2 pool 1 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743467 | CITE-seq: chip 2 pool 2 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743468 | CITE-seq: chip 2 pool 3 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743469 | CITE-seq: chip 2 pool 4 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743470 | CITE-seq: chip 2 pool 5 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743471 | CITE-seq: chip 2 pool 6 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743472 | CITE-seq: chip 2 pool 7 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743473 | CITE-seq: chip 2 pool 16 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 0 |
| GSM8743474 | TCR-seq: chip 1 pool 1 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743475 | TCR-seq: chip 1 pool 2 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743476 | TCR-seq: chip 1 pool 3 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743477 | TCR-seq: chip 1 pool 4 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743478 | TCR-seq: chip 1 pool 5 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743479 | TCR-seq: chip 1 pool 6 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743480 | TCR-seq: chip 1 pool 7 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743481 | TCR-seq: chip 1 pool 8 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743482 | TCR-seq: chip 2 pool 1 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743483 | TCR-seq: chip 2 pool 2 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743484 | TCR-seq: chip 2 pool 3 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743485 | TCR-seq: chip 2 pool 4 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743486 | TCR-seq: chip 2 pool 5 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743487 | TCR-seq: chip 2 pool 6 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743488 | TCR-seq: chip 2 pool 7 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |
| GSM8743489 | TCR-seq: chip 2 pool 16 | Tumor | tissue: Tumor; cell type: CD3+ T cells | RNA-Seq | 1 |

### GSE300147: Xenium Spatial Transcriptomics of Head and Neck Single Cell Carcinoma

- **type**: Other
- **summary**: Recent work has shown that the spatial organization of immune responses is a critical determinant of anti-tumor immunity. Here, we profiled ten head and neck squamous cell carcinoma (HNSCC) patient tumors and one ameloblastoma tumor using Xenium V1 spatial transcriptomics. The 10X genomics human multi-tissue and cancer gene expression panel targeting 377 genes was used in combination with 100 custom Xenium probes targeting patient-specific CDR3 regions of T cell receptors (TCRs) in T cells, additoinal T cell specific genes, HPV oncoprotein genes, and tumor genes of interest. This enabled the detection of 477 transcripts within each tumor sample at a single-cell resolution. For seven of the ten HNSCC samples, different tissue sections run on different days were analyzed as technical replicates. Together, these findings introduce a scalable platform for spatial clonal T cell analysis an...
- **overall_design**: Ten fresh-frozen HNSCC tumors, five of which were HPV+, were used for analysis. Seven of the ten tumors were run in replicate on different slides on different days for a total of 17 HNSCC tumor sections analyzed via Xenium spatial transcriptomics. One ameloblastoma tumor was also analysised via Xenium spatial transcriptomics.
- relation: BioProject: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1279130

| GSM | title | source | characteristics | library | n supp files |
|---|---|---|---|---|---|
| GSM9054471 | Patient 1, run 1 | HNSCC tumor | p16 status: Positive; recurrence: Recurrent; pack years: ... |  | 7 |
| GSM9054472 | Patient 9, run 1 | HNSCC tumor | p16 status: Positive; recurrence: Primary; pack years: 10... |  | 6 |
| GSM9054473 | Patient 9, run 2 | HNSCC tumor | p16 status: Positive; recurrence: Primary; pack years: 10... |  | 7 |
| GSM9054474 | Patient 12, run 1 | HNSCC tumor | p16 status: Positive; recurrence: Primary; pack years: 44... |  | 7 |
| GSM9054475 | Patient 12, run 2 | HNSCC tumor | p16 status: Positive; recurrence: Primary; pack years: 44... |  | 7 |
| GSM9054476 | Patient 13, run 1 | HNSCC tumor | p16 status: Positive; recurrence: Recurrent; pack years: ... |  | 6 |
| GSM9054477 | Patient 13, run 2 | HNSCC tumor | p16 status: Positive; recurrence: Recurrent; pack years: ... |  | 7 |
| GSM9054478 | Patient 15, run 1 | HNSCC tumor | p16 status: N/A; recurrence: Primary; pack years: 0; site... |  | 7 |
| GSM9054479 | Patient 17, run 1 | HNSCC tumor | p16 status: N/A; recurrence: Primary; pack years: 40; sit... |  | 6 |
| GSM9054480 | Patient 17, run 2 | HNSCC tumor | p16 status: N/A; recurrence: Primary; pack years: 40; sit... |  | 7 |
| GSM9054481 | Patient 19, run 1 | HNSCC tumor | p16 status: N/A; recurrence: Primary; pack years: 80; sit... |  | 7 |
| GSM9054482 | Patient 19, run 2 | HNSCC tumor | p16 status: N/A; recurrence: Primary; pack years: 80; sit... |  | 7 |
| GSM9054483 | Patient 20, run 1 | HNSCC tumor | p16 status: Negative; recurrence: Primary; pack years: 42... |  | 7 |
| GSM9054484 | Patient 20, run 2 | HNSCC tumor | p16 status: Negative; recurrence: Primary; pack years: 42... |  | 7 |
| GSM9054485 | Patient 23, run 1 | HNSCC tumor | p16 status: N/A; recurrence: Primary; pack years: 45; sit... |  | 7 |
| GSM9054486 | Patient 28, run 1 | HNSCC tumor | p16 status: Positive; recurrence: Recurrent; pack years: ... |  | 7 |
| GSM9054487 | Patient 28, run 2 | HNSCC tumor | p16 status: Positive; recurrence: Recurrent; pack years: ... |  | 7 |
| GSM9054488 | Patient 10, run 1 | Ameloblastoma | p16 status: N/A; recurrence: Primary; pack years: NA; sit... |  | 6 |

## Warnings

- GSE179572/GSM5420752_pt24_matrix.mtx.gz: BadGzipFile: Not a gzipped file (b'<?')
- GSE238071: zero-byte files: GSE238071/GSM7658221_UKF260_SPTCR13_CORRECTED_UMI_CORRRECTED_IGB_TRABDG.csv.gz
- GSE238071/GSM7658227_UKF334_SPTCR14_CORRECTED_UMI_CORRRECTED_IGB_TRABDG.csv.gz: BadGzipFile: Not a gzipped file (b'<?')

