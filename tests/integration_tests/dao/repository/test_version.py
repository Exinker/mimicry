import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@pytest.mark.asyncio
async def test_version(
    session_factory: async_sessionmaker[AsyncSession],
    postgrtee_version: str,
):
    query = text('SELECT VERSION()')
    async with session_factory() as session:
        result = (await session.execute(query)).scalar()

    assert result.startswith(f'PostgreSQL {postgrtee_version}')
