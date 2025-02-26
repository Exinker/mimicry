from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import (
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from mimicry.config import CONFIG
from mimicry.dao.repository.models import UserModel
from mimicry.dao.exceptions import (
    ConnectionRepositoryError,
    MigrationRepositoryError,
    RepositoryError,
)
from mimicry.dto import UserDTO


def connection(method):

    async def wrapper(self, *args, **kwargs):

        async with self.session() as session:
            try:
                result = await method(self, *args, **kwargs, session=session)
                return result

            except OperationalError as error:
                await session.rollback()
                raise ConnectionRepositoryError from error

            except ProgrammingError as error:
                await session.rollback()
                raise MigrationRepositoryError from error

            except Exception as error:
                raise RepositoryError from error

            finally:
                await session.close()

    return wrapper


class Repository:

    def __init__(self):

        self._engine = create_async_engine(
            url=CONFIG.database.url,
            echo=CONFIG.database.echo,
        )
        self._session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    def session(self) -> AsyncSession:
        return self._session_factory()

    @connection
    async def add_user(self, user: UserDTO, session: AsyncSession) -> None:

        session.add(UserModel(**user.model_dump()))

        await session.commit()

    async def get_users(self) -> Sequence[UserDTO]:

        query = select(UserModel)
        async with self.session() as session:
            users = session.execute(query)

            print()
