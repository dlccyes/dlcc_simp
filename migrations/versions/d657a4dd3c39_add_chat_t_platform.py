"""add chat_t platform

Revision ID: d657a4dd3c39
Revises: 392fa6d7cec1
Create Date: 2022-04-23 03:38:46.786042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd657a4dd3c39'
down_revision = '392fa6d7cec1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_t', sa.Column('platform', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat_t', 'platform')
    # ### end Alembic commands ###
