"""create chat_t

Revision ID: f41bdaeb563a
Revises: 21a04d95a9f5
Create Date: 2022-04-22 20:31:17.827965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f41bdaeb563a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chat_t',
        sa.Column("name", sa.String),
        sa.Column("msg_count", sa.Integer),
        sa.Column("last_msg_time", sa.DateTime)
    )

def downgrade():
    op.drop_table('chat_t')
