"""Phone number column adding for the users table.

Revision ID: bc817acadc29
Revises: 
Create Date: 2026-09-17 22:48:00.706563

"""
from typing import Sequence, Union

from alembic import op
from pydantic_core.core_schema import nullable_schema
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc817acadc29'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String,nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
