"""Added bets table clubs and schedule

Revision ID: 77057e2597bb
Revises: 7bff5434b1de
Create Date: 2024-01-08 13:16:05.374440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77057e2597bb'
down_revision: Union[str, None] = '7bff5434b1de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('premier_league_clubs',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('abbreviation', sa.String(), nullable=False),
    sa.Column('record', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('premier_league_schedules',
    sa.Column('home_team', sa.String(), nullable=False),
    sa.Column('away_team', sa.String(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.Column('date_event', sa.DateTime(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=False),
    sa.Column('away_score', sa.Integer(), nullable=False),
    sa.Column('league_name', sa.String(), nullable=False),
    sa.Column('event_location', sa.String(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['clubs.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['clubs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('premier_league_schedules')
    op.drop_table('premier_league_clubs')
    # ### end Alembic commands ###
