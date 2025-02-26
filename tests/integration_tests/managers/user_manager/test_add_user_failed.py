from typing import Callable

import pytest
from testcontainers.postgres import PostgresContainer

from mimicry.dao.repository import UserModel
from mimicry.managers import UserManager
from mimicry.managers.exceptions import UserManagerError


@pytest.mark.asyncio
async def test_add_user_when_connection_database_failed(
    container: PostgresContainer,
    user_manager: UserManager,
    user_factory: Callable[[UserModel], bool],
):
    container.stop(force=True)

    with pytest.raises(UserManagerError):
        await user_manager.add_user(
            user=user_factory(),
        )


@pytest.mark.asyncio
async def test_add_user_when_migration_failed(
    user_manager: UserManager,
    user_factory: Callable[[UserModel], bool],
):

    with pytest.raises(UserManagerError):
        await user_manager.add_user(
            user=user_factory(),
        )
