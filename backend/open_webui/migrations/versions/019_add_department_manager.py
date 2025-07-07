"""Add department manager functionality

Revision ID: 019_add_department_manager
Revises: 922e7a387820
Create Date: 2024-12-26 20:56:00.000000

"""

from alembic import op
import sqlalchemy as sa

revision = "019_add_department_manager"
down_revision = "9f0c9cd09105"
branch_labels = None
depends_on = None


def upgrade():
    # Add created_by column to group table
    op.add_column('group', sa.Column('created_by', sa.Text(), nullable=True))
    
    # Add managed_by column to group table
    op.add_column('group', sa.Column('managed_by', sa.Text(), nullable=True))
    
    # Add department column to group table
    op.add_column('group', sa.Column('department', sa.Text(), nullable=True))


def downgrade():
    # Remove columns from group table
    op.drop_column('group', 'created_by')
    op.drop_column('group', 'managed_by')
    op.drop_column('group', 'department')