import os, redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

async def init_rate_limiter(app: FastAPI):
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis = aioredis.from_url(redis_url, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)
