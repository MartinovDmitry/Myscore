"""Created payments table

Revision ID: 2329916bc37c
Revises: 2504ec1f8d6b
Create Date: 2024-01-03 21:44:25.359647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2329916bc37c'
down_revision: Union[str, None] = '2504ec1f8d6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('bonuses', sa.Integer(), nullable=False),
    sa.Column('replenishment_at', sa.DateTime(), nullable=False),
    sa.Column('withdrawal_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.CheckConstraint('count >= 0', name='check_count_positive'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    # ### end Alembic commands ###
