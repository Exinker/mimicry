from pydantic_settings import BaseSettings

from mimicry.config.database_config import DatabaseConfig


class Config(BaseSettings):

    database: DatabaseConfig = DatabaseConfig()


CONFIG = Config()
