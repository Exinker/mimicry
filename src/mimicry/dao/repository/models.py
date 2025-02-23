import uuid
from datetime import datetime, timezone
from functools import partial
from typing import Any, Mapping

from sqlalchemy import UUID
from sqlalchemy.orm import (
    ColumnProperty,
    DeclarativeBase,
    Mapped,
    class_mapper,
    mapped_column,
)


class BaseModel(DeclarativeBase):

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=partial(datetime.now, tz=timezone.utc),
    )

    def asdict(self) -> Mapping[str, Any]:
        cls = self.__class__

        content = dict()
        for property in class_mapper(cls).iterate_properties:
            if isinstance(property, ColumnProperty):
                content[property.key] = getattr(self, property.key)

        return content

    def __str__(self) -> str:
        cls = self.__class__

        return '{name}({content})'.format(
            name=cls.__name__,
            content=', '.join([
                f'{key}={value}'
                for key, value in self.asdict().items()
            ])
        )


class UserModel(BaseModel):
    __tablename__ = 'users'

    nickname: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=False)
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    update_at: Mapped[datetime] = mapped_column(
        default=partial(datetime.now, tz=timezone.utc),
        onupdate=partial(datetime.now, tz=timezone.utc),
    )


class ReferenceModel(BaseModel):
    __tablename__ = 'references'

    url_full: Mapped[str] = mapped_column(unique=True)
    url_short: Mapped[str] = mapped_column(unique=True)
