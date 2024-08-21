import random
from redis_client import redis_client


def create_random_verification_code() -> int:
    return random.randint(100000, 999999)


async def stor_code(key: str, value: int):
    redis_client.set(key, 30, value)


async def check_code(key: str, value: int) -> bool:
    code = redis_client.get(key)
    if code == None:
        return False

    try:
        # Attempt to convert the Redis response to an int for comparison
        return int(code) == value  # type: ignore
    except (ValueError, TypeError):
        # If conversion fails, return False
        return False
