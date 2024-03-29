"""empty message

Revision ID: c78457db3d02
Revises: 
Create Date: 2021-08-01 12:20:03.944348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c78457db3d02'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_name', sa.String(length=32), nullable=False),
    sa.Column('display_name', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('joined', sa.DateTime(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('picture', sa.Text(), nullable=False),
    sa.Column('last_name_change', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('post',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('author_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('last_edit', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('tags', sa.ARRAY(postgresql.UUID(as_uuid=True)), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.ForeignKeyConstraint(['author_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('sandbox',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('author_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['author_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sandbox')
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###
