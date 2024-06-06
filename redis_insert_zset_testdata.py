import redis
import time

def generate_test_data(num_elements):
    data = {f'member_{i}': i for i in range(num_elements)}
    return data

def insert_zset_data(redis_host, redis_port, db, key, data):
    r = redis.Redis(host=redis_host, port=redis_port, db=db)

    # if exists key then delete 
    r.delete(key)

    total_time = 0
    times = []

    for member, score in data.items():
        start_time = time.time()
        r.zadd(key, {member: score})
        end_time = time.time()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        total_time += elapsed_time

    avg_time = total_time / len(data)
    print(f'Inserted {len(data)} elements into {key}')
    print(f'Total time: {total_time:.4f} seconds')
    print(f'Average time per ZADD: {avg_time:.6f} seconds')

    return times

if __name__ == "__main__":
    redis_host = 'localhost'
    redis_port = 6379
    db = 1
    key = 'test_zset'
    num_elements = 100000

    # 生成测试数据
    data = generate_test_data(num_elements)

    # 插入 Zset 数据并测量时间
    insert_zset_data(redis_host, redis_port, db, key, data)
