"""added is_active & activation code fields to the users model

Revision ID: bf5b9a097665
Revises: 0a8ad19324b7
Create Date: 2024-07-20 22:45:01.497845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf5b9a097665'
down_revision = '0a8ad19324b7'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to the users table
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.false()))
    op.add_column('users', sa.Column('activation_code', sa.Integer(), nullable=True))


def downgrade():
    # Remove the columns from the users table
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'activation_code')
