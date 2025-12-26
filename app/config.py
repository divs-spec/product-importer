import os

DATABASE_URL = os.environ.get("DATABASE_URL")
REDIS_URL = os.environ.get("REDIS_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL environment variable is required")
