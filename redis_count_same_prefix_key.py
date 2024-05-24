import redis

# 连接到 Redis
r = redis.Redis(host='xxxxxxxxx', port=6379, db=1)

# initial cursor and count 0 
cursor = '0'
count = 0

# use scan command to find same prefix key
while True:
    cursor, keys = r.scan(cursor=cursor, match='core_proxy_user_first_proxy_count_*', count=1000)
    count += len(keys)
    if cursor == '0':  # cursor return 0 , end for loop
        break

print("匹配到的键的数量:", count)
