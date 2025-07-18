from typing import Final
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: Final = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

REDIS_URL: Final = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
