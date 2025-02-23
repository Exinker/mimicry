import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope='session')
def postgrtee_version() -> str:
    return '11'


@pytest.fixture(scope='session')
def container(
    postgrtee_version: str,
) -> PostgresContainer:

    container = PostgresContainer(
        image=f'postgres:{postgrtee_version}',
        driver='psycopg',
    )
    container.start()

    yield container

    container.stop()


@pytest.fixture(scope='session')
def engine(
    container: PostgresContainer,
) -> AsyncEngine:
    return create_async_engine(
        url=container.get_connection_url(),
    )


@pytest.fixture(scope='session')
def session_factory(
    engine: AsyncEngine,
) -> AsyncSession:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
    )
