# 06_scenic_summary.R
library(Seurat)
lung <- readRDS('../../lung_mac_scenic_subclustered.rds'); DefaultAssay(lung) <- 'AUC'
kidney <- readRDS('../../kidney_mac_scenic_final.rds'); DefaultAssay(kidney) <- 'AUC'
lung_var <- apply(GetAssayData(lung, assay = 'AUC', layer = 'counts'), 1, var)
kidney_var <- apply(GetAssayData(kidney, assay = 'AUC', layer = 'counts'), 1, var)
shared <- intersect(names(sort(lung_var, decreasing = TRUE))[1:150],
                    names(sort(kidney_var, decreasing = TRUE))[1:150])
cat('Shared TFs (Top 150):', length(shared), '\n')
lung_avg <- rowMeans(GetAssayData(lung, assay = 'AUC', layer = 'counts')[shared, ])
kidney_avg <- rowMeans(GetAssayData(kidney, assay = 'AUC', layer = 'counts')[shared, ])
ct <- cor.test(lung_avg, kidney_avg, method = 'spearman')
cat('Cross-organ Rho:', round(ct$estimate, 3), '; p:', ct$p.value, '\n')
