"""empty message

Revision ID: 6764b4aa4d39
Revises: d7d0a1a4701e
Create Date: 2021-06-28 23:06:48.909311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6764b4aa4d39'
down_revision = 'd7d0a1a4701e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contract', type_='foreignkey')
    op.drop_column('contract', 'organization')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract', sa.Column('organization', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'contract', 'organization', ['organization'], ['id'])
    # ### end Alembic commands ###