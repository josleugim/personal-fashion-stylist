"""add_hobbies_and_sports_to_profiles

Revision ID: 8efdc0b503f5
Revises: 06c9ff4c2d63
Create Date: 2026-04-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision: str = '8efdc0b503f5'
down_revision: Union[str, Sequence[str], None] = '06c9ff4c2d63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('profiles', sa.Column('hobbies', ARRAY(sa.String()), nullable=True))
    op.add_column('profiles', sa.Column('sports', ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('profiles', 'sports')
    op.drop_column('profiles', 'hobbies')
