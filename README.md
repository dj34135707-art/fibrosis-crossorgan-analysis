# Cross-organ SPP1+ macrophage-myofibroblast axis in human fibrotic diseases

Analysis code for the manuscript:
**"Cross-organ single-cell and bulk transcriptomics reveals a conserved SPP1+ macrophage-myofibroblast axis in human fibrotic diseases"**

## Overview

This repository contains the R and Python scripts used for:
1. Single-cell RNA-seq analysis (lung SCP2879, kidney GSE209781)
2. pySCENIC gene regulatory network inference
3. Bulk transcriptomic integration (GSE47460, GSE76882, GSE22459, GSE84044)
4. Module scoring (ssGSEA), immune deconvolution (xCell), and clinical association analysis

## Data availability

All raw datasets are publicly available:

| Dataset | Organ | Accession | N |
|---------|-------|-----------|---|
| scRNA-seq | Lung | SCP2879 | 61,067 immune + 16,071 stromal |
| scRNA-seq | Kidney | GSE209781 | 18,782 |
| Bulk | Lung | GSE47460 | 429 |
| Bulk | Kidney | GSE76882 | 274 |
| Bulk | Kidney | GSE22459 | 65 |
| Bulk | Liver | GSE84044 | 124 |

Processed intermediate files are available at Zenodo:
**DOI: [10.5281/zenodo.23150833]** (https://doi.org/10.5281/zenodo.23150833)

## Requirements

- R >= 4.4.0
- Python >= 3.8 (for pySCENIC)
- See `sessionInfo.txt` for full R package versions

### Key R packages
- Seurat (v5)
- harmony
- GSVA
- IOBR
- pROC
- glmnet
- igraph

### Python packages
- pySCENIC (v0.12.1)
- arboreto (GRNBoost2)
- scanpy

## Usage

Scripts are numbered in execution order:

```bash
# Single-cell module scoring
Rscript 01_single_cell/03_module_scoring.R
Rscript 01_single_cell/05_ligand_receptor.R

# pySCENIC
python 02_pySCENIC/run_grnboost2_lung.py
python 02_pySCENIC/run_grnboost2_kidney.py
python 02_pySCENIC/run_ctx_lung.py
python 02_pySCENIC/run_ctx_kidney.py
Rscript 02_pySCENIC/shared_TF_analysis.R

# Bulk analysis
Rscript 03_bulk_analysis/02_ssGSEA_scoring.R
Rscript 03_bulk_analysis/04_clinical_association.R

# xCell deconvolution
Rscript 04_xcell/xcell_deconvolution.R
```

## Notes on reproducibility

- Random seeds are set with `set.seed(123)` in all permutation tests
- All file paths are set at the top of each script (search for `BASE_DIR`)
- Analysis was performed on R 4.4.x; minor version differences should not affect results

## Citation

If you use this code, please cite:
> Dan J, et al. Cross-organ single-cell and bulk transcriptomics reveals a conserved SPP1+ macrophage-myofibroblast axis in human fibrotic diseases. *BMC Bioinformatics* (submitted).

## Contact

Jie Dan  
Department of Gastrointestinal Surgery  
The People's Hospital of Leshan  
Email: 34135705@qq.com  
ORCID: 0009-0005-1559-3675
