"""add content column to post table

Revision ID: 74933ed734e8
Revises: 4351a83e007c
Create Date: 2025-09-29 18:55:25.441874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74933ed734e8'
down_revision: Union[str, Sequence[str], None] = '4351a83e007c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
