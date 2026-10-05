import pandas as pd
from arboreto.algo import grnboost2
from arboreto.utils import load_tf_names
import warnings

# 屏蔽烦人的警告
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    expr_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/kidney_mac_500.csv"
    tf_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/db/allTFs_hg38.txt"
    out_file = "C:/2026.10.2/Fibrosis_Project/SCENIC/output/kidney_adjacencies.csv"

    print("🔄 正在加载肾脏表达矩阵...")
    ex_matrix = pd.read_csv(expr_file, index_col=0)
    
    # 🔄 【关键修复】：自动识别并纠正矩阵方向！
    if ex_matrix.shape[0] > ex_matrix.shape[1]:
        print("🔄 检测到矩阵方向为 [基因 x 细胞]，正在自动转置为 pySCENIC 要求的 [细胞 x 基因] 格式...")
        ex_matrix = ex_matrix.T
    
    # 🛠️ 检查并剔除重名基因
    print("🛠️ 正在检查并剔除重名基因...")
    duplicates = ex_matrix.columns.duplicated()
    if duplicates.sum() > 0:
        print(f"⚠️ 发现并剔除了 {duplicates.sum()} 个重复的基因列！")
        ex_matrix = ex_matrix.loc[:, ~duplicates]
    
    # 🧹 过滤沉默基因提速
    print("🧹 正在清理全为 0 的无效基因 (超级提速中)...")
    expressed_cells_per_gene = (ex_matrix > 0).sum(axis=0)
    ex_matrix = ex_matrix.loc[:, expressed_cells_per_gene >= 5]
    
    print("🔄 正在加载转录因子列表...")
    tf_names = load_tf_names(tf_file)
    tf_names = [tf for tf in tf_names if tf in ex_matrix.columns]
    
    # 这次你会看到正确的数字：500个细胞，一万多个基因！
    print(f"📊 最终清洗后的矩阵大小: {ex_matrix.shape[0]} 个细胞, {ex_matrix.shape[1]} 个有效基因")
    print(f"🧬 成功匹配到 {len(tf_names)} 个有效转录因子")
    
    print("\n🚀 开始高强度计算肾脏调控网络！这次数据方向正确，绝对稳！")
    
    try:
        adj = grnboost2(expression_data=ex_matrix, tf_names=tf_names)
        
        print("\n💾 计算完成！正在保存结果...")
        adj.to_csv(out_file, index=False)
        print(f"✅ 大功告成！共找到 {len(adj)} 条调控边。")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")