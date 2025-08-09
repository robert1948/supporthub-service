from __future__ import annotations
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250809_0002_add_created_at'
down_revision = '20250809_0001_init'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('tickets', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))
    op.add_column('messages', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('messages', 'created_at')
    op.drop_column('tickets', 'created_at')
