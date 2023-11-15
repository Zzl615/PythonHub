import asyncio
import aioredis

async def clear_cache(app_id: str):
    result = False
    redis_dsn = "redis://127.0.0.1:6379/0"
    redis = aioredis.from_url(redis_dsn)
    keys = await redis.keys(f"{app_id}*")
    print(keys)
    if keys:
        result = await redis.delete(*keys)
        print(result)
    return bool(result)


if __name__ == "__main__":
    asyncio.run(clear_cache("gouhuo_"))

