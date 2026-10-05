import pandas as pd
from arboreto.algo import grnboost2
from arboreto.utils import load_tf_names
import warnings

# 屏蔽烦人的警告
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    expr_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/lung_final.csv"
    tf_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/db/allTFs_hg38.txt"
    out_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/output/lung_adjacencies.csv"

    print("🔄 正在加载表达矩阵 (这需要一点时间)...")
    ex_matrix = pd.read_csv(expr_file, index_col=0)
    
    # 【核心提速区】：过滤掉全是 0 的无效基因，防止程序崩溃！
    print("🧹 正在清理全为 0 的无效基因 (超级提速中)...")
    expressed_cells_per_gene = (ex_matrix > 0).sum(axis=0)
    ex_matrix = ex_matrix.loc[:, expressed_cells_per_gene >= 5]
    
    print("🔄 正在加载转录因子列表...")
    tf_names = load_tf_names(tf_file)
    tf_names = [tf for tf in tf_names if tf in ex_matrix.columns]
    
    print(f"📊 过滤后的矩阵大小: {ex_matrix.shape[0]} 个细胞, {ex_matrix.shape[1]} 个有效基因")
    print(f"🧬 成功匹配到 {len(tf_names)} 个有效转录因子")
    
    print("\n🚀 开始高强度计算调控网络！")
    print("⚠️ 提示: 垃圾变量已清理，导致报错的 Client 已移除，这次绝对稳！")
    print("⚠️ 请耐心等待十几到几十分钟，直到看到【大功告成】！\n")
    
    try:
        # 使用最原生、最稳定的推断模式
        adj = grnboost2(expression_data=ex_matrix, tf_names=tf_names)
        
        print("\n💾 计算完成！正在保存结果...")
        adj.to_csv(out_file, index=False)
        print(f"✅ 大功告成！共找到 {len(adj)} 条调控边。")
        print(f"📁 文件已保存至: {out_file}")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")