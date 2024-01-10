"""Updeted premier_league_schedules table

Revision ID: 4b19e9bc90e4
Revises: 77057e2597bb
Create Date: 2024-01-08 15:24:59.210757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b19e9bc90e4'
down_revision: Union[str, None] = '77057e2597bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('premier_league_schedules', 'home_score',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('premier_league_schedules', 'away_score',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('premier_league_schedules_away_team_id_fkey', 'premier_league_schedules', type_='foreignkey')
    op.drop_constraint('premier_league_schedules_home_team_id_fkey', 'premier_league_schedules', type_='foreignkey')
    op.create_foreign_key(None, 'premier_league_schedules', 'premier_league_clubs', ['away_team_id'], ['id'])
    op.create_foreign_key(None, 'premier_league_schedules', 'premier_league_clubs', ['home_team_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'premier_league_schedules', type_='foreignkey')
    op.drop_constraint(None, 'premier_league_schedules', type_='foreignkey')
    op.create_foreign_key('premier_league_schedules_home_team_id_fkey', 'premier_league_schedules', 'clubs', ['home_team_id'], ['id'])
    op.create_foreign_key('premier_league_schedules_away_team_id_fkey', 'premier_league_schedules', 'clubs', ['away_team_id'], ['id'])
    op.alter_column('premier_league_schedules', 'away_score',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('premier_league_schedules', 'home_score',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###