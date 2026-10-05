# 05_xcell.R
library(IOBR)
for (organ in c('lung','k2','liver')) {
  expr <- readRDS(paste0('../../expr_final_', organ, '.rds'))
  xcell <- deconvo_tme(eset = 2^expr, method = 'xcell', arrays = FALSE)
  saveRDS(xcell, paste0('../../xcell_', organ, '.rds'))
  cat(organ, 'xCell done\n')
}
mac_lung <- readRDS('../../bulk_lung_mac_fibro_correlation.rds')$mac_lung
xcell_lung <- readRDS('../../xcell_lung.rds')
xcell_mat <- as.data.frame(xcell_lung); rownames(xcell_mat) <- xcell_mat$ID; xcell_mat$ID <- NULL
for (ct in c('B-cells_xCell','Class-switched_memory_B-cells_xCell')) {
  if (ct %in% colnames(xcell_mat)) {
    ct_val <- as.numeric(xcell_mat[names(mac_lung), ct])
    ct_res <- cor.test(mac_lung, ct_val, method = 'spearman')
    cat(ct, ': Rho =', round(ct_res$estimate, 3), '; p =', ct_res$p.value, '\n')
  }
}
