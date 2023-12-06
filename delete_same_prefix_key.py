import redis

# connect Redis
r = redis.Redis(host='redis-film-new.bxbb5w.ng.0001.ape1.cache.amazonaws.com', port=6379, db=1)

# prefix
prefix = "core_sns_user_current_browsed_recommend_film_pool_"

# scan all of match prefix key
for key in r.scan_iter(f"{prefix}*"):
    # count key nummber
    count = r.scard(key)

    # check each key elements more than 20000
    if count > 20000:
        print(f"Deleting key: {key.decode('utf-8')}, Size: {count}")
        r.delete(key)
