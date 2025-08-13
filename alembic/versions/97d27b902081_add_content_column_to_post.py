"""add content column to post

Revision ID: 97d27b902081
Revises: 2a4d808f2d95
Create Date: 2025-08-13 13:43:14.605361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97d27b902081'
down_revision: Union[str, Sequence[str], None] = '2a4d808f2d95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("post", "content")
    pass
