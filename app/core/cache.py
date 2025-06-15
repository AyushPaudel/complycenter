import redis
from redis.exceptions import RedisError, ConnectionError, AuthenticationError
from fastapi import HTTPException
from core.logger import get_logger
from core.config import settings

logger = get_logger("redis")


def get_redis():
    """
    FastAPI dependency to provide a Redis connection.
    Yields a Redis client and ensures proper cleanup.
    """
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
        )
        # Test connection
        r.ping()
        logger.debug("Redis connection established")
        yield r
    except ConnectionError as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise HTTPException(
            status_code=503, detail="Redis unavailable, please try again later"
        )
    except AuthenticationError as e:
        logger.error(f"Redis authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Redis authentication failed")
    except RedisError as e:
        logger.error(f"Unexpected Redis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        try:
            r.close()
            logger.debug("Redis connection closed")
        except Exception as e:
            logger.warning(f"Error closing Redis connection: {str(e)}")
