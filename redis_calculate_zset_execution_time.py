import redis
import time

# Connect to Redis
client = redis.Redis(host='xxxxxxxxx', port=6379, db=1)

# Prompt the user to enter the key name
zset_key = input("Enter the key name for your ZSET: ")

# Measure execution time for ZREVRANGEBYSCORE
start_time = time.time()
highest_scored_element = client.zrevrangebyscore(zset_key, '+inf', '-inf', start=0, num=1, withscores=True)
end_time = time.time()

# Calculate execution time
execution_time = end_time - start_time

# Output the result
print(f"Highest scored element: {highest_scored_element}")
print(f"Execution time: {execution_time} seconds")
