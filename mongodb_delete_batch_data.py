import pandas as pd
from pymongo import MongoClient

# 讀取 CSV 文件
file_path = 'chunk_14.csv'  # 替換成你的 CSV 文件路徑
df = pd.read_csv(file_path, header=None, names=['user_id'])
user_ids = df['user_id'].tolist()


# 設定 MongoDB 連接
client = MongoClient('mongodb://gcp_replica:123qwe@172.31.43.229:27017/apple_record',
                     authSource='admin',  # 認證數據庫
                     authMechanism='SCRAM-SHA-256')  # 認證機制

# 選擇數據庫和 collection
db = client['apple_record']
collection = db['core_user_mduserloginrecord']

# 批量刪除
batch_size = 20000  # 每批處理的 user_id 數量
for i in range(0, len(user_ids), batch_size):
    batch = user_ids[i:i+batch_size]
    result = collection.delete_many({'user_id': {'$in': batch}})
    print(f"Batch {i // batch_size + 1}: Deleted {result.deleted_count} documents.")
