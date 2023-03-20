from dataclasses import dataclass

import logging
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    type: Optional[str] = None
    connector: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    login: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None

    @property
    def uri(self):
        if self.type in ('mysql', 'postgresql'):
            url = (
                f'{self.type}+{self.connector}://'
                f'{self.login}:{self.password}'
                f'@{self.host}:{self.port}/{self.name}'
            )
        elif self.type == 'sqlite':
            url = (
                f'{self.type}://{self.path}'
            )
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        logger.debug(url)
        return url
