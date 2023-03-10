"""add is_enabled to category

Revision ID: 679164fc710f
Revises: 9563221113a3
Create Date: 2022-12-25 19:35:31.559107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '679164fc710f'
down_revision = '9563221113a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('is_active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'is_active')
    # ### end Alembic commands ###
