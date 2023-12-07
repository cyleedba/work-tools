import redis

# connect Redis
r = redis.Redis(host='redis-sv.bxbb5w.ng.0001.ape1.cache.amazonaws.com', port=6379, db=1)

# prefix
prefix = "core_sns_user_browse_tiktok_short_video_record_*"

# Initialize a counter for deleted keys
deleted_keys = 0

# scan all of match prefix key
for key in r.scan_iter(f"{prefix}*"):
    # count key nummber
    count = r.scard(key)

    # check each key elements more than 20000
    if count > 20000:
        # Get the memory usage of the key
        memory_usage = r.memory_usage(key)

        # Check if the memory usage is more than 1000000 bytes
        if memory_usage > 850000:
            print(f"Deleting key: {key.decode('utf-8')}, Size: {count}, Memory Usage: {memory_usage} bytes")
            r.delete(key)

            # Increment the deleted keys counter
#            deleted_keys += 1

            # Break the loop if 1000 keys have been deleted
#            if deleted_keys >= 1000:
#                break
