import redis
import random

# 連接到 Redis
client = redis.Redis(host='redis-db.bxbb5w.ng.0001.ape1.cache.amazonaws.com', port=6379, db=0)

# your hash table key
hash_key = 'test_hash'

# 插入 10 萬筆數據
for i in range(30000):
    user_id = i  # 假設 user_id 從 0 開始遞增
    count = random.randint(1, 100)  # 隨機生成一個 count 值
    client.hset(hash_key, f"{user_id}", count)

print("數據插入完成")
