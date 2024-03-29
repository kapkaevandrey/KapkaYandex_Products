"""First migration

Revision ID: 0e6f51c0d745
Revises:
Create Date: 2022-06-15 23:59:49.543697

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy

revision = '0e6f51c0d745'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'node',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column(
            'type', sa.Enum('offer', 'category', name='producttype'),
            nullable=False
        ),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column(
            'id', fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False
        ),
        sa.Column(
            'parent_id', fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=True
        ),
        sa.ForeignKeyConstraint(['parent_id'], ['node.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'user',
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column(
            'id', fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table(
        'nodehistory',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column(
            'type',
            sa.Enum('offer', 'category', name='producttype'),
            nullable=False
        ),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'node_id', fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False
        ),
        sa.Column(
            'parent_id', fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=True
        ),
        sa.Column('update_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('nodehistory')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('node')
