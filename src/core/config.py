from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

LOG_FORMAT = "%(levelname)s:\t%(message)s"
REDIS_EXPIRE = 7200


class Config(BaseSettings):
    db_url: PostgresDsn
    redis: RedisDsn
    log_level: str = 'DEBUG'


config = Config()
