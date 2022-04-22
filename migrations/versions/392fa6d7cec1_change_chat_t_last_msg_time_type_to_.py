"""change chat_t last_msg_time type to string

Revision ID: 392fa6d7cec1
Revises: 5df36a5b38a8
Create Date: 2022-04-23 00:50:18.450315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '392fa6d7cec1'
down_revision = '5df36a5b38a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chat_t', 'last_msg_time',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(length=50),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chat_t', 'last_msg_time',
               existing_type=sa.String(length=50),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###
