import multiprocessing.process
import sys
from pyscenic.cli.pyscenic import main

# 🛠️ 【终极底层补丁】：修复 Python 3.10 多进程参数冲突 Bug
try:
    import multiprocessing_on_dill.process as mod_process
    if hasattr(mod_process, 'BaseProcess'):
        _orig_mod_bootstrap = mod_process.BaseProcess._bootstrap
        def _patched_mod_bootstrap(self, parent_sentinel=None):
            return _orig_mod_bootstrap(self)
        mod_process.BaseProcess._bootstrap = _patched_mod_bootstrap
except ImportError:
    pass

_orig_bootstrap = multiprocessing.process.BaseProcess._bootstrap
def _patched_bootstrap(self, parent_sentinel=None):
    return _orig_bootstrap(self)
multiprocessing.process.BaseProcess._bootstrap = _patched_bootstrap

if __name__ == '__main__':
    # 注意：这里我们换成了刚刚洗白生成的 kidney_clean.csv
    sys.argv = [
        'pyscenic', 'ctx',
        'C:/2026.10.2/Fibrosis_Project/SCENIC/output/kidney_adjacencies.csv',
        'C:/2026.10.2/Fibrosis_Project/SCENIC/db/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather',
        '--annotations_fname', 'C:/2026.10.2/Fibrosis_Project/SCENIC/db/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl',
        '--expression_mtx_fname', 'C:/2026.10.2/Fibrosis_Project/SCENIC/kidney_clean.csv', 
        '--output', 'C:/2026.10.2/Fibrosis_Project/SCENIC/output/kidney_regulons.csv',
        '--num_workers', '4'
    ]
    
    print("🚀 肾脏数据 CTX 补丁加载成功！正在启动 4 核加速分析...")
    main()
    print("✅ 肾脏 CTX 步骤大功告成！kidney_regulons.csv 已成功生成！")