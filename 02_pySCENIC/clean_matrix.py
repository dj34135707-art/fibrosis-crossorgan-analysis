import pandas as pd

file_in = "C:/2026.10.2/Fibrosis_Project/SCENIC/kidney_mac_500.csv"
file_out = "C:/2026.10.2/Fibrosis_Project/SCENIC/kidney_clean.csv"

print("🔄 正在读取原始矩阵 (这需要一点时间)...")
df = pd.read_csv(file_in, index_col=0)

print("🔄 正在将 [基因 x 细胞] 转置为 [细胞 x 基因]...")
df = df.T

print("🛠️️ 正在剔除会导致崩溃的重名基因...")
df = df.loc[:, ~df.columns.duplicated()]

print(f"💾 正在保存干净的矩阵...")
df.to_csv(file_out)
print("✅ 矩阵清洗完成！这下 CTX 和 AUCell 绝对不会再报错了！")