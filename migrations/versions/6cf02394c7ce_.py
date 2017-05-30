"""Add organization to Orders

Revision ID: 6cf02394c7ce
Revises: d2e8cf6703da
Create Date: 2017-05-30 16:31:54.057566

"""

# revision identifiers, used by Alembic.
revision = '6cf02394c7ce'
down_revision = 'd2e8cf6703da'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('organization', sa.String(length=80), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'organization')
    ### end Alembic commands ###
