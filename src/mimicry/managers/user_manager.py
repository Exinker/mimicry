from collections.abc import Sequence

from mimicry.dao.repository import Repository
from mimicry.dao.exceptions import RepositoryError
from mimicry.managers.exceptions import UserManagerError
from mimicry.dto import UserDTO


def user_manager_factory(
    repository: Repository,
) -> 'UserManager':

    return UserManager(
        repository=repository,
    )


class UserManager():

    create = user_manager_factory

    def __init__(
        self,
        repository: Repository,
    ) -> None:
        self._repository = repository

    async def add_user(self, user: UserDTO) -> None:

        try:
            await self._repository.add_user(user=user)
        except RepositoryError as error:
            raise UserManagerError from error

    async def get_users(self) -> Sequence[UserDTO]:

        users = await self._repository.get_users()
        return users
