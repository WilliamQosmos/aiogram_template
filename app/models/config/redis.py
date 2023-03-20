from dataclasses import dataclass

import logging
from typing import Optional

from redis.asyncio.client import Redis

logger = logging.getLogger(__name__)


@dataclass
class RedisConfig:
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    db: Optional[int] = None

    @property
    def uri(self):
        if self.user:
            url = (
                f'redis://'
                f'{self.user}:{self.password}'
                f'@{self.host}:{self.port}/{self.db}'
            )
        else:
            raise ValueError("Username Redis not available")
        logger.debug(url)
        return url

    @property
    def create_redis(self) -> Redis:
        """
        Implementation of the Redis protocol.
        """
        if self.user:
            return Redis(host=self.user, port=self.port, username=self.user, password=self.password, db=self.db)
        else:
            return Redis(host=self.user, port=self.port, password=self.password, db=self.db)
