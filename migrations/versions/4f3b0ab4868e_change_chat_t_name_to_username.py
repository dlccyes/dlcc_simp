"""change chat_t name to username

Revision ID: 4f3b0ab4868e
Revises: f41bdaeb563a
Create Date: 2022-04-22 20:40:19.141080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3b0ab4868e'
down_revision = 'f41bdaeb563a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('chat_t', 'name', new_column_name='username')


def downgrade():
    op.alter_column('chat_t', 'username', new_column_name='name')