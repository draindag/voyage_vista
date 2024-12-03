"""adding check constraint on role in users table

Revision ID: b00d6f2a62db
Revises: 6dd2be8d2c53
Create Date: 2024-11-22 16:29:37.199196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b00d6f2a62db'
down_revision = '6dd2be8d2c53'
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем CHECK CONSTRAINT к существующей таблице users
    op.create_check_constraint(
        'users_role_check',
        'users',
        "role IN ('visitor', 'moderator', 'admin')"
    )


def downgrade():
    # Удаляем CHECK CONSTRAINT если он существует
    op.drop_constraint('users_role_check', 'users', type_='check')