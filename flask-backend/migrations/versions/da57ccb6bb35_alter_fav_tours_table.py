"""alter fav_tours table

Revision ID: da57ccb6bb35
Revises: b00d6f2a62db
Create Date: 2024-11-22 23:51:57.226517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da57ccb6bb35'
down_revision = 'b00d6f2a62db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fav_tours', schema=None) as batch_op:
        batch_op.drop_constraint('fav_tours_tour_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('fav_tours_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'tours', ['tour_id'], ['tour_id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fav_tours', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fav_tours_user_id_fkey', 'users', ['user_id'], ['user_id'])
        batch_op.create_foreign_key('fav_tours_tour_id_fkey', 'tours', ['tour_id'], ['tour_id'])

    # ### end Alembic commands ###