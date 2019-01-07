"""add permission

Revision ID: c03ee1139877
Revises: d8fb5903fe30
Create Date: 2019-01-06 17:46:09.604811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c03ee1139877'
down_revision = 'd8fb5903fe30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permission', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permission')
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###