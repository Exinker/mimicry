from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):

    host: str = Field(alias='DB_HOST')
    port: str = Field(alias='DB_PORT')
    username: str = Field(alias='DB_USERNAME')
    password: SecretStr = Field(alias='DB_PASSWORD')
    name: str = Field(alias='DB_NAME')
    echo: bool = Field(False, alias='DB_ECHO')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def url(self) -> str:
        return 'postgresql+psycopg://{username}:{password}@{host}:{port}/{name}'.format(
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            name=self.name,
        )
