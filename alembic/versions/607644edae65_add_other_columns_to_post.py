"""add other columns to post

Revision ID: 607644edae65
Revises: b91f0271b0cf
Create Date: 2025-08-13 14:06:35.512944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '607644edae65'
down_revision: Union[str, Sequence[str], None] = 'b91f0271b0cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts",  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
