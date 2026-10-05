# 02_bulk_ssgsea.R
library(GSVA)
mac_genes <- c('SPP1','TREM2','CD9','GPNMB','APOE','LGALS3')
fibro_genes <- c('POSTN','COL1A1','COL1A2','ACTA2','FN1','CTHRC1')
for (organ in c('lung','k2','liver')) {
  expr <- readRDS(paste0('../../expr_final_', organ, '.rds'))
  mac <- gsva(ssgseaParam(expr, list(Mac_SPP1 = mac_genes)), verbose = FALSE)[1, ]
  fibro <- gsva(ssgseaParam(expr, list(Fibro_Myo = fibro_genes)), verbose = FALSE)[1, ]
  ct <- cor.test(mac, fibro, method = 'spearman')
  cat(organ, 'Mac-Fibro Rho:', round(ct$estimate, 3), '; p:', ct$p.value, '\n')
}
