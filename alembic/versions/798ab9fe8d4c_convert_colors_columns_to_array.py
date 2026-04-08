"""convert_colors_columns_to_array

Revision ID: 798ab9fe8d4c
Revises: f447ba2783d3
Create Date: 2026-04-07 22:31:28.260935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '798ab9fe8d4c'
down_revision: Union[str, Sequence[str], None] = 'f447ba2783d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_USING = (
    "CASE WHEN {col} IS NULL OR {col} = '{{}}' "
    "THEN ARRAY[]::text[] "
    "ELSE string_to_array(trim(both '{{}}' from {col}), ',') "
    "END"
)


def upgrade() -> None:
    op.alter_column(
        'profiles', 'favorite_colors',
        type_=postgresql.ARRAY(sa.String),
        postgresql_using=_USING.format(col='favorite_colors'),
    )
    op.alter_column(
        'profiles', 'colors_to_avoid',
        type_=postgresql.ARRAY(sa.String),
        postgresql_using=_USING.format(col='colors_to_avoid'),
    )


def downgrade() -> None:
    op.alter_column(
        'profiles', 'favorite_colors',
        type_=sa.String(length=255),
        postgresql_using="array_to_string(favorite_colors, ',')",
    )
    op.alter_column(
        'profiles', 'colors_to_avoid',
        type_=sa.String(length=255),
        postgresql_using="array_to_string(colors_to_avoid, ',')",
    )
