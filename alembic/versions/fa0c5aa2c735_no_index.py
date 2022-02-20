"""no_index

Revision ID: fa0c5aa2c735
Revises: 9ef7afbe192c
Create Date: 2022-01-20 08:04:09.751266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa0c5aa2c735'
down_revision = '9ef7afbe192c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_cpf', table_name='user')
    op.drop_index('ix_user_id', table_name='user')
    op.drop_index('ix_user_name', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_user_name', 'user', ['name'], unique=False)
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    op.create_index('ix_user_cpf', 'user', ['cpf'], unique=False)
    # ### end Alembic commands ###