import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from mimicry.config import CONFIG
from mimicry.config.database_config import DatabaseConfig
from mimicry.dao.repository.models import ReferenceModel


@pytest.fixture(scope='function', autouse=True)
def setup_database(
    container: PostgresContainer,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv('DB_HOST', container.get_container_host_ip())
    monkeypatch.setenv('DB_PORT', container.get_exposed_port(5432))
    monkeypatch.setenv('DB_USERNAME', container.username)
    monkeypatch.setenv('DB_PASSWORD', container.password)
    monkeypatch.setenv('DB_NAME', container.dbname)
    monkeypatch.setattr(CONFIG, 'database', DatabaseConfig())

    command.upgrade(
        config=Config('alembic.ini'),
        revision='head',
    )


@pytest.fixture
def url_full(
    faker,
) -> str:
    return faker.uri()


@pytest.fixture
def url_short(
    faker,
) -> str:
    return faker.uri()


@pytest.mark.asyncio
async def test_add_reference(
    session_factory: async_sessionmaker[AsyncSession],
    url_full: str,
    url_short: str,
):
    async with session_factory() as session:
        session.add(ReferenceModel(
            url_full=url_full,
            url_short=url_short,
        ))
        await session.commit()

    async with session_factory() as session:
        item = (await session.execute(select(ReferenceModel))).scalar()

    assert item.url_full == url_full
    assert item.url_short == url_short
