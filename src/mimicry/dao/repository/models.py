import uuid
from datetime import datetime, timezone
from functools import partial

from sqlalchemy import UUID
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
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
