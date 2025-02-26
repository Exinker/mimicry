from typing import Callable

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from mimicry.dao.repository import UserModel
from mimicry.dto import UserDTO
from mimicry.managers import UserManager


@pytest.fixture(autouse=True)
def setup(
    database_factory,
):
    database_factory(
        migration='head',
    )


@pytest.fixture
def check_user_in_database(
    session_factory: async_sessionmaker[AsyncSession],
) -> Callable[[UserModel], bool]:

    async def inner(
        __expected: UserModel,
    ) -> bool:

        query = select(UserModel)
        async with session_factory() as session:
            item = (await session.execute(query)).scalars().one()
            user = UserDTO.model_validate(item)

        return user == __expected

    return inner


@pytest.mark.asyncio
async def test_add_user(
    user_manager: UserManager,
    user_factory: Callable[[UserModel], bool],
    check_user_in_database: Callable[[UserModel], bool],
):
    user = user_factory()

    await user_manager.add_user(
        user=user,
    )

    assert await check_user_in_database(user)
