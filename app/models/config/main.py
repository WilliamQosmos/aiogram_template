import json
from pathlib import Path
from typing import Optional, Any, Dict, Tuple, Type, List

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from redis.asyncio.client import Redis
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from app.enums import BotApiType
from app.enums import StorageType


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get('env_file_encoding')
        file_content_json = json.loads(
            Path('app/config/superusers.json').read_text(encoding)
        )
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8')

    TG_BOT_TOKEN: str
    LOGGING_CHAT_ID: str
    WISH_CHAT_ID: str
    STORAGE_TYPE: StorageType
    BOTAPI_TYPE: BotApiType
    BOTAPI_URL: str
    BOTAPI_FILE_URL: str

    WEB_SERVER_HOST: str
    WEB_SERVER_PORT: int
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str
    BASE_WEBHOOK_URL: str
    WEBHOOK_SSL_CERT: str
    WEBHOOK_SSL_PRIV: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int

    superusers: List[int]

    @property
    def db_uri(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def create_redis(self) -> Redis:
        """
        Implementation of the Redis protocol.
        """
        return Redis(host=self.REDIS_HOST, port=self.REDIS_PORT, password=self.REDIS_PASSWORD, db=self.REDIS_DB)

    def create_bot_session(self) -> Optional[AiohttpSession]:
        if self.botapi_is_local:
            return AiohttpSession(api=self.create_server())
        return None

    @property
    def botapi_is_local(self) -> bool:
        return self.BOTAPI_TYPE == BotApiType.local

    def create_server(self) -> TelegramAPIServer:
        if self.BOTAPI_TYPE != BotApiType.local:
            raise RuntimeError("can create only local botapi server")
        return TelegramAPIServer(
            base=f"{self.BOTAPI_URL}/bot{{token}}/{{method}}",
            file=f"{self.BOTAPI_FILE_URL}{{path}}",
        )

    @property
    def storage_is_local(self) -> bool:
        return self.STORAGE_TYPE == StorageType.memory

    @property
    def create_db_pool(self) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(url=make_url(self.db_uri),
                                     pool_pre_ping=True)  # , pool_size=15, max_overflow=25)
        pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        return pool

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            JsonConfigSettingsSource(settings_cls),
            init_settings,
            file_secret_settings,
        )

