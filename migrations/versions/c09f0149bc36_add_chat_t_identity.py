"""add chat_t identity

Revision ID: c09f0149bc36
Revises: 4f3b0ab4868e
Create Date: 2022-04-22 21:00:48.680630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c09f0149bc36'
down_revision = '4f3b0ab4868e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chat_t', sa.Column('identity', sa.String))


def downgrade():
    op.drop_column('chat_t', 'identity')
