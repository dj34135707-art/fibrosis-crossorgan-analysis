# 04_ligand_receptor.R
library(Seurat)
genes <- c('SPP1','CD44','ITGAV','ITGB1','ITGB5')
for (obj_file in c('lung_mac_annotated.rds','mac_dkd.rds')) {
  obj <- readRDS(paste0('../../', obj_file)); obj <- JoinLayers(obj)
  for (g in genes) {
    if (g %in% rownames(obj)) {
      expr <- as.numeric(GetAssayData(obj, layer = 'data')[g, ])
      cat(obj_file, g, ':', round(mean(expr > 0) * 100, 1), '%\n')
    }
  }
}
