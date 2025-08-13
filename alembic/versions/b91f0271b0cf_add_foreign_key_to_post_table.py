"""add foreign key to post table

Revision ID: b91f0271b0cf
Revises: a299a0253b83
Create Date: 2025-08-13 13:57:58.215238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b91f0271b0cf'
down_revision: Union[str, Sequence[str], None] = 'a299a0253b83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", 
        local_cols=['user_id'], remote_cols=['id'], ondelete='Restrict'
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
