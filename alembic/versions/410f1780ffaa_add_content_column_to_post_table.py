"""add content column to post table

Revision ID: 410f1780ffaa
Revises: 2bac47768ae2
Create Date: 2025-05-11 17:51:09.736418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '410f1780ffaa'
down_revision: Union[str, None] = '2bac47768ae2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
