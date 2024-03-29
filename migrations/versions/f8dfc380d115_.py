"""empty message

Revision ID: f8dfc380d115
Revises: 6964ac905fa0
Create Date: 2021-08-12 20:13:15.711219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f8dfc380d115'
down_revision = '6964ac905fa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_like',
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('post_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['post_uuid'], ['post.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('user_uuid', 'post_uuid')
    )
    op.drop_column('post', 'likes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('likes', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_table('post_like')
    # ### end Alembic commands ###
