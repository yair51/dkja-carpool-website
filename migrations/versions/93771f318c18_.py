"""empty message

Revision ID: 93771f318c18
Revises: 918c95eb8628
Create Date: 2022-03-18 17:54:14.287366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93771f318c18'
down_revision = '918c95eb8628'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('child', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.drop_constraint('child_user_id_fkey', 'child', type_='foreignkey')
    op.create_foreign_key(None, 'child', 'parent', ['parent_id'], ['id'])
    op.drop_column('child', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('child', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'child', type_='foreignkey')
    op.create_foreign_key('child_user_id_fkey', 'child', 'user', ['user_id'], ['id'])
    op.drop_column('child', 'parent_id')
    # ### end Alembic commands ###
