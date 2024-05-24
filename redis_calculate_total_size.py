import redis
import threading
from concurrent.futures import ThreadPoolExecutor

# 連接到Redis服務器
r = redis.Redis(host='xxxxxxxxxx', port=6379, db=1)

def calculate_size_for_keys(keys):
    total_size = 0
    for key in keys:
        total_size += r.memory_usage(key)
    return total_size

def calculate_total_size(pattern, count=1000, num_threads=10):
    total_size = 0
    cursor = 0
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        while True:
            cursor, keys = r.scan(cursor=cursor, match=pattern, count=count)
            if keys:
                futures.append(executor.submit(calculate_size_for_keys, keys))
            if cursor == 0:
                break
        for future in futures:
            total_size += future.result()
    return total_size

# 計算前綴為 core_sns_user_browse_tiktok_short_video_record_* 的所有鍵的總大小
pattern = 'core_sns_user_browse_tiktok_short_video_record_*'
total_size = calculate_total_size(pattern)

print(f'Total size of keys with prefix "{pattern}": {total_size} bytes')
