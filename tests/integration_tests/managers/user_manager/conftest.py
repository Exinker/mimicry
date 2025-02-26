from typing import Callable

import pytest

from mimicry.dao.repository import (
    Repository,
    UserModel,
)
from mimicry.dto import UserDTO
from mimicry.managers import UserManager


@pytest.fixture
def user_manager() -> UserManager:
    return UserManager(
        repository=Repository(),
    )


@pytest.fixture
def user_factory(faker) -> Callable[[UserModel], bool]:

    def inner(**fields) -> UserDTO:

        data = dict(
            nickname=faker.name().lower().replace(' ', '_'),
            password=faker.password(),
            email=faker.email(),
        )
        data.update(fields)

        return UserDTO(**data)

    return inner
