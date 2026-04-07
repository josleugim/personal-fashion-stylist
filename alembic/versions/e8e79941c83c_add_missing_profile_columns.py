"""Add missing profile columns

Revision ID: e8e79941c83c
Revises: ae155ea77b25
Create Date: 2026-04-06 11:52:58.488252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8e79941c83c'
down_revision: Union[str, Sequence[str], None] = 'ae155ea77b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


logo_tolerance_enum = sa.Enum('HIGH', 'Medium', 'Low', name='logotolerance')


def upgrade() -> None:
    """Upgrade schema."""
    logo_tolerance_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('profiles', sa.Column('budget', sa.String(length=100), nullable=True))
    op.add_column('profiles', sa.Column('logo_tolerance', logo_tolerance_enum, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('profiles', 'logo_tolerance')
    op.drop_column('profiles', 'budget')
    logo_tolerance_enum.drop(op.get_bind(), checkfirst=True)
