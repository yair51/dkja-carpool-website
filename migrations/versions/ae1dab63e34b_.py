"""empty message

Revision ID: ae1dab63e34b
Revises: 
Create Date: 2022-03-11 09:17:41.072090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae1dab63e34b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('family')
    # ### end Alembic commands ###


def downgrade():
    pass
    # # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='family_pkey')
    )
    # ### end Alembic commands ###
