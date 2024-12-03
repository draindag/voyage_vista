"""add admin user to users table

Revision ID: 7d8d9a2b788f
Revises: 7c330acec352
Create Date: 2024-11-25 11:49:49.335248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d8d9a2b788f'
down_revision = '7c330acec352'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO public.users (user_id, login, email, password, role)
        VALUES ('b2baca0d-d53a-4c8c-b9ee-febf4a3772a2', 'admin', 'admin@example.com', 'scrypt:32768:8:1$I46FwljVOX8XLFU9$0756cdbfcf626ab7b9826892e4cc281f7f9492a353f7d30346c91447f7724117f035ac859e8d76852f1df6781e0254b5d1bd3b345307ddf10173af22779e950f', 'admin');
    """)

def downgrade():
    op.execute("""
        DELETE FROM public.users
        WHERE user_id = 'b2baca0d-d53a-4c8c-b9ee-febf4a3772a2';
    """)