"""initial migration

Revision ID: d5f361e0412e
Revises:
Create Date: 2025-02-23 14:34:48.131001

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d5f361e0412e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "references",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("url_full", sa.String(), nullable=False),
        sa.Column("url_short", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url_full"),
        sa.UniqueConstraint("url_short"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("update_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("nickname"),
    )


def downgrade() -> None:
    op.drop_table("references")
    op.drop_table("users")
