"""empty message

Revision ID: 9f9ef65b377e
Revises: fa5b4d313051
Create Date: 2023-05-31 14:23:08.917959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f9ef65b377e'
down_revision = 'fa5b4d313051'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Dateregistration', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('Sex', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('Birth_Date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('Ava', sa.LargeBinary(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('Ava')
        batch_op.drop_column('Birth_Date')
        batch_op.drop_column('Sex')
        batch_op.drop_column('Dateregistration')

    # ### end Alembic commands ###
