import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from mimicry.config import CONFIG
from mimicry.config.database_config import DatabaseConfig


@pytest.fixture(scope='session')
def postgrtee_version() -> str:
    return '11'


@pytest.fixture(scope='function')
def container(
    postgrtee_version: str,
) -> PostgresContainer:

    container = PostgresContainer(
        image=f'postgres:{postgrtee_version}',
        driver='psycopg',
    )
    container.start()
    container

    yield container

    if container.get_wrapped_container().status == 'running':
        container.stop()


@pytest.fixture(scope='function')
def engine(
    container: PostgresContainer,
) -> AsyncEngine:
    return create_async_engine(
        url=container.get_connection_url(),
    )


@pytest.fixture(scope='function')
def session_factory(
    engine: AsyncEngine,
) -> AsyncSession:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
    )


@pytest.fixture(scope='function')
def database_factory(
    container: PostgresContainer,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv('DB_HOST', container.get_container_host_ip())
    monkeypatch.setenv('DB_PORT', container.get_exposed_port(5432))
    monkeypatch.setenv('DB_USERNAME', container.username)
    monkeypatch.setenv('DB_PASSWORD', container.password)
    monkeypatch.setenv('DB_NAME', container.dbname)
    monkeypatch.setattr(CONFIG, 'database', DatabaseConfig())

    def inner(
        migration: str | None = 'head',
    ) -> None:

        if migration:
            command.upgrade(
                config=Config('alembic.ini'),
                revision=migration,
            )

    return inner
