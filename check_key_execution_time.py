import redis
import time

# 連接到 Redis
client = redis.Redis(host='localhost', port=6379, db=0)

# 請求用戶輸入鍵和字段/成員
key = input("請輸入鍵 (key): ")
field_or_member = input("請輸入字段或成員 (field_or_member): ")

# 測量開始時間
start_time = time.time()

# 獲取鍵的類型
key_type = client.type(key).decode('utf-8')

# 根據鍵的類型來取值
if key_type == 'hash':
    value = client.hget(key, field_or_member)
elif key_type == 'zset':
    value = client.zscore(key, field_or_member)
elif key_type == 'set':
    value = client.sismember(key, field_or_member)
elif key_type == 'string':
    value = client.get(key)
else:
    value = None

# 測量結束時間
end_time = time.time()

# 計算執行時間
execution_time = end_time - start_time

# 輸出結果
if value is not None:
    if isinstance(value, bytes):
        value = value.decode('utf-8')  # 從字節解碼為字符串
    print(f"The value of '{field_or_member}' in the {key_type} '{key}' is: {value}")
else:
    print(f"The '{field_or_member}' does not exist in the {key_type} '{key}'")
print(f"Execution time: {execution_time} seconds")
