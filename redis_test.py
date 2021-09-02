import redis
from main import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


r = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

print(r.keys())


"""
for key in r.scan_iter():
    # delete the key
    r.delete(key)
"""