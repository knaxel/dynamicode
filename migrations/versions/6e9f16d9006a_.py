"""empty message

Revision ID: 6e9f16d9006a
Revises: f8acfb5a060f
Create Date: 2021-08-17 15:25:31.711269

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e9f16d9006a'
down_revision = 'f8acfb5a060f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'author_uuid',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'author_uuid',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
