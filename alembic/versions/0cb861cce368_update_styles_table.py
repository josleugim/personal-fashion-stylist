"""Update styles table

Revision ID: 0cb861cce368
Revises: 11041d84285c
Create Date: 2026-03-25 22:50:58.715180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cb861cce368'
down_revision: Union[str, Sequence[str], None] = '11041d84285c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    strictness_enum = sa.Enum('HIGH', 'MEDIUM', 'LOW', name='strictnesslevel')
    strictness_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('styles', sa.Column('strictness', strictness_enum, nullable=False))
    op.add_column('styles', sa.Column('palette', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('styles', sa.Column('avoid', sa.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('styles', 'avoid')
    op.drop_column('styles', 'palette')
    op.drop_column('styles', 'strictness')
    sa.Enum(name='strictnesslevel').drop(op.get_bind(), checkfirst=True)
