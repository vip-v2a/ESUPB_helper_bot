import os
import json
import logging
import redis
from dotenv import load_dotenv

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

load_dotenv()

Redis_db = None

logger = logging.getLogger(__name__)


def Redis_db_connection(need_new_key:bool=True):
    global Redis_db

    if Redis_db is None:
        Redis_db = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )

    new_key = 0
    if need_new_key:
        Redis_db.incr("key_counter")
        new_key = Redis_db.get("key_counter")
    
    return Redis_db, new_key


def save_danger_to_db(user_id, user_data):
    
    data = {
        "contacts": user_data["contacts"],
        "danger_type": user_data["danger_type"],
        "place": user_data["place"],
        "danger": user_data["danger"],
        "awared": user_data["awared"]
    }

    db, key = Redis_db_connection()
    db.hset(user_id, key, json.dumps(data))


def save_improvement_to_db(user_id, user_data):
    data = {
        "contacts" : user_data["contacts"],
        "impr" : user_data["improvement"]
    }

    db, key = Redis_db_connection()
    db.hset(user_id, key, json.dumps(data))

