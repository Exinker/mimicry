from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from mimicry.config import CONFIG


class ReferenceRepository:

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
