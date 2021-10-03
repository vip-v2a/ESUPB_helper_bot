import redis,json
from MyHandlers.db_handler import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


r = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

# r.hset('my_id', 1, 'my_number')
# h_len = r.hlen('my_id2')
# r.hset('my_id2', h_len , 'my_number')
# r.hdel('my_id', h_len , 'my_number')

# user_keys = r.hkeys('my_id3')
# if user_keys:
# r.incr('counter')
# print(r.get('counter'))


# data = {'contacts' : 'тут текст', 'impr' : 'тут текст'}
# r = Redis_r_connection()
# r.incr('impr_counter')
# ckey = r.get('counter')
# r.hset("my_id3", ckey, json.dumps(data))

# print(r.keys())
# for key in r.keys():
#     print(r.hkeys(key))
# print(r.hkeys(b'824177756'))
# print(r.hkeys(b'265392956'))

print(json.loads(r.hget('265392956', '8')))
# print(json.loads(r.hget('265392956', '9')))
# print(json.loads(r.hget('824177756', '3')))
# print(r.get('danger_counter'))
# print(r.hkeys('my_id3'))
# print(json.loads(r.hget('my_id3', ckey)))



# for key in r.keys():
    # r.delete(key)
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