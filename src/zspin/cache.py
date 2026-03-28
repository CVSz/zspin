from __future__ import annotations

import os

import redis
from redis import Redis


def get_cache() -> Redis:
    """Build a Redis client from environment variables."""
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )


r = get_cache()
