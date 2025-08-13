"""create post table

Revision ID: 2a4d808f2d95
Revises: 
Create Date: 2025-08-13 13:28:45.717057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a4d808f2d95'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    # sa.Column('content', sa.String(), nullable=False),
                    # sa.Column('published', sa.Boolean(), server_default='True', nullable=False),
                    # # sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='Restrict'), nullable=False),
                    # sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
                    
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
