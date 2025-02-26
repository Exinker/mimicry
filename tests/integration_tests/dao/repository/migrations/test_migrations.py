import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from mimicry.dao.repository.models import ReferenceModel


@pytest.fixture(autouse=True)
def setup_config(database_factory):
    database_factory(
        migration='head',
    )


@pytest.fixture
def url_full(faker) -> str:
    return faker.uri()


@pytest.fixture
def url_short(faker) -> str:
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
