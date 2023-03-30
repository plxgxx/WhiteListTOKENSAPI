"""empty message

Revision ID: 232ebbc16807
Revises: b6c2d56ca144
Create Date: 2023-03-03 23:02:04.963582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '232ebbc16807'
down_revision = 'b6c2d56ca144'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cresto_passes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('owner_id', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('mintedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cresto_passes')
    # ### end Alembic commands ###
