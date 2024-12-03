"""adding unique constraint in offers_tours table

Revision ID: 7af3caf8587e
Revises: fe55ec194425
Create Date: 2024-11-25 11:49:49.335248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7af3caf8587e'
down_revision = 'fe55ec194425'
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем UNIQUE CONSTRAINT для столбцов tour_id и offer_id
    op.create_unique_constraint(
        'uq_tour_id_offer_id',  # Имя уникального ограничения
        'offers_tours',         # Имя таблицы
        ['tour_id', 'offer_id'] # Столбцы, к которым применяется ограничение
    )


def downgrade():
    # Удаляем UNIQUE CONSTRAINT, если он существует
    op.drop_constraint('uq_tour_id_offer_id', 'offers_tours', type_='unique')