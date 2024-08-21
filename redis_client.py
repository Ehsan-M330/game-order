import redis
from redis.client import Redis

redis_client: Redis = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True
)
