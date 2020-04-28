"""add result success flag

Revision ID: 5ff234245e25
Revises: 564204310105
Create Date: 2020-04-24 09:11:05.719753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ff234245e25'
down_revision = '564204310105'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('success', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('result', 'success')
    # ### end Alembic commands ###
