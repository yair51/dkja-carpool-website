"""empty message

Revision ID: c9597accf5b7
Revises: 93771f318c18
Create Date: 2022-03-18 18:07:12.701243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9597accf5b7'
down_revision = '93771f318c18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('arrival', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.drop_constraint('arrival_user_id_fkey', 'arrival', type_='foreignkey')
    op.create_foreign_key(None, 'arrival', 'parent', ['parent_id'], ['id'])
    op.drop_column('arrival', 'user_id')
    op.add_column('vehicle', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.drop_constraint('vehicle_user_id_fkey', 'vehicle', type_='foreignkey')
    op.create_foreign_key(None, 'vehicle', 'parent', ['parent_id'], ['id'])
    op.drop_column('vehicle', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicle', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.create_foreign_key('vehicle_user_id_fkey', 'vehicle', 'user', ['user_id'], ['id'])
    op.drop_column('vehicle', 'parent_id')
    op.add_column('arrival', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'arrival', type_='foreignkey')
    op.create_foreign_key('arrival_user_id_fkey', 'arrival', 'user', ['user_id'], ['id'])
    op.drop_column('arrival', 'parent_id')
    # ### end Alembic commands ###