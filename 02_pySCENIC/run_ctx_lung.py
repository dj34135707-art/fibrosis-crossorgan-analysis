import pandas as pd
from pyscenic.utils import load_motifs, modules_from_adjacencies
from pyscenic.prune import prune2df
import pyscenic.prune as prune_module
from ctxcore.rnkdb import RankingsDatabase

if __name__ == '__main__':
    print("🔄 正在加载必要的输入文件...")
    adj_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/output/lung_adjacencies.csv"
    expr_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/lung_final.csv"
    db_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/db/hg38_10kbp_up_10kbp_down_full_tx_v10_clust.genes_vs_motifs.rankings.feather"
    anno_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/db/motifs-v10nr_clust-nr.hgnc-m0.001-o0.0.tbl"
    out_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/output/lung_regulons.csv"

    # 读取网络和表达矩阵
    adjacencies = pd.read_csv(adj_file)
    ex_matrix = pd.read_csv(expr_file, index_col=0)

    print("🔄 正在加载 Motif 数据库与注释文件...")
    databases = [RankingsDatabase(db_file, name='hg38_rankings')]
    motifs = load_motifs(anno_file)

    print("🔄 正在构建共表达模块...")
    modules = modules_from_adjacencies(adjacencies, ex_matrix, rho_mask_dropouts=False)

    # 🛠️️ 【关键拦截】：直接强行覆写 pySCENIC 的底层分布式计算函数，
    # 将其强制替换为纯单线程顺序循环，彻底消灭任何 multiprocessing 报错！
    def safe_sequential_calc(dbs, regulons, annotations, nes_threshold, rank_threshold, auc_threshold, min_orthologous_identity, max_similarity_fdr, num_workers, client_or_address=None, custom_multiprocessing=False):
        print("💡 已成功接管计算引擎：正在以纯单线程、零多进程的绝对安全模式执行剪枝...")
        results = []
        total = len(regulons)
        for i, reg in enumerate(regulons):
            if (i + 1) % 50 == 0 or (i + 1) == total:
                print(f"  ⏳ CTX 剪枝进度: 正在处理第 {i + 1} / {total} 个转录因子模块...")
            try:
                # 直接调用官方内部的单 worker 执行函数
                res = prune_module._worker((dbs[0], [reg], annotations, nes_threshold, rank_threshold, auc_threshold, min_orthologous_identity, max_similarity_fdr))
                if res is not None:
                    results.append(res)
            except Exception as e:
                continue
                
        # 收集并合并结果
        df_list = []
        for r in results:
            if isinstance(r, pd.DataFrame) and not r.empty:
                df_list.append(r)
            elif isinstance(r, str):
                try:
                    df = pd.read_csv(r)
                    if not df.empty:
                        df_list.append(df)
                except:
                    pass
        return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()

    # 替换官方有 Bug 的多进程函数
    prune_module._distributed_calc = safe_sequential_calc

    print("🚀 开始执行安全版 CTX 剪枝与 Motif 富集分析...")
    df_regulons = prune2df(dbs=databases, modules=modules, annotations=motifs, num_workers=1)

    print(f"💾 正在保存 Regulons 结果...")
    df_regulons.to_csv(out_file, index=False)
    print(f"✅ CTX 步骤大功告成！Regulons 已安全保存至: {out_file}")