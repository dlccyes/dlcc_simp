"""add chat_t id

Revision ID: 5df36a5b38a8
Revises: c09f0149bc36
Create Date: 2022-04-22 21:04:52.828120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5df36a5b38a8'
down_revision = 'c09f0149bc36'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chat_t', sa.Column('id', sa.Integer(), primary_key=True))

def downgrade():
    op.drop_column('chat_t', 'id')