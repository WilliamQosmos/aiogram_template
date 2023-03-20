
from app.models.config.redis import RedisConfig


def load_redis_config(redis_dict: dict) -> RedisConfig:
    return RedisConfig(
        host=redis_dict.get('host', None),
        port=redis_dict.get('port', None),
        user=redis_dict.get('user', None),
        password=redis_dict.get('password', None),
        db=redis_dict.get('db', None),
    )
