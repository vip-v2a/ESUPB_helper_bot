import redis
from MyHandlers.db_handler import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


r = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

# r.hset('my_id', 'my_value', 'my_number')
print(r.keys())
print(r.hkeys('my_id'))

"""
for key in r.scan_iter():
    # delete the key
    r.delete(key)
"""
"""
import redis
r = redis.Redis("localhost", 6379)
for key in r.scan_iter():
       print key



redis_server.hset(key, value, number)
key[value] = number
"""