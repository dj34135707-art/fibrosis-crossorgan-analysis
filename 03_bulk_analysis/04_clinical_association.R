# 03_clinical_regression.R
library(GEOquery); library(GSVA)
gse <- getGEO(filename = '../../Lung_GSE47460/GSE47460-GPL14550_series_matrix.txt.gz', getGPL = FALSE)
clin <- pData(gse)
meta <- data.frame(
  sample = rownames(clin),
  FVC = as.numeric(as.character(clin$`%predicted fvc (pre-bd):ch1`)),
  DLCO = as.numeric(as.character(clin$`%predicted dlco:ch1`)),
  Age = as.numeric(as.character(clin$`age:ch1`)),
  Sex = as.factor(clin$`Sex:ch1`),
  Smoking = as.factor(clin$`smoker?:ch1`)
)
lung_res <- readRDS('../../bulk_lung_mac_fibro_correlation.rds')
meta$Score <- lung_res$mac_lung[meta$sample]
meta <- na.omit(meta)
print(summary(lm(FVC ~ Score + Age + Sex + Smoking, data = meta)))
print(summary(lm(DLCO ~ Score + Age + Sex + Smoking, data = meta)))
