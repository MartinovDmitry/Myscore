from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class BetsMain(Base):
    __tablename__ = 'bets'

    home_team_id: Mapped[int] = mapped_column(ForeignKey('premier_league_clubs.id'))
    away_team_id: Mapped[int] = mapped_column(ForeignKey('premier_league_clubs.id'))
    event_name: Mapped[str]
    moneyline_away: Mapped[int]
    