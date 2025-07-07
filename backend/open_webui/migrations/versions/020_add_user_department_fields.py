"""Add department fields to user table

Revision ID: 020_add_user_department_fields
Revises: 019_add_department_manager
Create Date: 2024-12-26 21:38:00.000000

"""

from alembic import op
import sqlalchemy as sa

revision = "020_add_user_department_fields"
down_revision = "019_add_department_manager"
branch_labels = None
depends_on = None


def upgrade():
    # Check if columns already exist before adding them
    from sqlalchemy import inspect
    from alembic import context
    
    conn = context.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('user')]
    
    # Add department column to user table if it doesn't exist
    if 'department' not in columns:
        op.add_column('user', sa.Column('department', sa.String(), nullable=True))
    
    # Add managed_by column to user table if it doesn't exist
    if 'managed_by' not in columns:
        op.add_column('user', sa.Column('managed_by', sa.String(), nullable=True))


def downgrade():
    # Remove columns from user table
    op.drop_column('user', 'department')
    op.drop_column('user', 'managed_by')