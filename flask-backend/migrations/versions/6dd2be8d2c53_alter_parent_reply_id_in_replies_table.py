"""alter parent_reply_id in replies table

Revision ID: 6dd2be8d2c53
Revises: c8a8af90765b
Create Date: 2024-11-22 15:59:34.400575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dd2be8d2c53'
down_revision = 'c8a8af90765b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('replies', schema=None) as batch_op:
        batch_op.alter_column('parent_reply_id',
               existing_type=sa.UUID(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('replies', schema=None) as batch_op:
        batch_op.alter_column('parent_reply_id',
               existing_type=sa.UUID(),
               nullable=False)

    # ### end Alembic commands ###
