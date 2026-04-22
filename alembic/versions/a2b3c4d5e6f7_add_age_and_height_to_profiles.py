"""add_age_and_height_to_profiles

Revision ID: a2b3c4d5e6f7
Revises: 8efdc0b503f5
Create Date: 2026-04-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2b3c4d5e6f7'
down_revision: Union[str, Sequence[str], None] = '8efdc0b503f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('profiles', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('profiles', sa.Column('height', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('profiles', 'height')
    op.drop_column('profiles', 'age')
