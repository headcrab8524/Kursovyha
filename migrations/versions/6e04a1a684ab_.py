"""empty message

Revision ID: 6e04a1a684ab
Revises: a58e43ae2a1a
Create Date: 2023-06-06 14:20:15.381583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e04a1a684ab'
down_revision = 'a58e43ae2a1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mod_views',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Modid', sa.Integer(), nullable=True),
    sa.Column('AuthorId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AuthorId'], ['user.id'], name=op.f('fk_mod_views_AuthorId_user')),
    sa.ForeignKeyConstraint(['Modid'], ['mod.id'], name=op.f('fk_mod_views_Modid_mod')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_mod_views'))
    )
    op.drop_table('mod_vievs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mod_vievs',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('Modid', sa.INTEGER(), nullable=True),
    sa.Column('AuthorId', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['AuthorId'], ['user.id'], ),
    sa.ForeignKeyConstraint(['Modid'], ['mod.id'], ),
    sa.PrimaryKeyConstraint('id', name='pk_mod_vievs')
    )
    op.drop_table('mod_views')
    # ### end Alembic commands ###
