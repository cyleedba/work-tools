import pandas as pd

# pymongo 有bson 檔案大小的限制 超過16MB 就會報錯
# 設置 CSV 文件路徑和拆分大小
file_path = 'anonymous_user.csv'  # 替換為您的文件路徑
chunk_size = 500000  # 每個小文件的行數，根據需要調整

# 讀取大型 CSV 文件，並分批拆分
for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
    chunk.to_csv(f'chunk_{i}.csv', index=False)
