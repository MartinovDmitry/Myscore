from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped

from db_helper import Base


class PremierLeagueSchedule(Base):
    __tablename__ = 'premier_league_schedules'

    home_team: Mapped[str] = mapped_column()
    away_team: Mapped[str] = mapped_column()
    home_team_id: Mapped[int] = mapped_column(ForeignKey('premier_league_clubs.id'))
    away_team_id: Mapped[int] = mapped_column(ForeignKey('premier_league_clubs.id'))
    date_event: Mapped[datetime] = mapped_column()
    home_score: Mapped[Optional[int]] = mapped_column(default=0)
    away_score: Mapped[Optional[int]] = mapped_column(default=0)
    league_name: Mapped[str]
    #  --Can't found the solution for concatenation values of columns-- #
    # event_name: Mapped[str] = mapped_column(
    #     insert_default=func.concat(home_team, ' at ', away_team, ' - ', date_event),
    #     onupdate=func.concat(home_team, ' at ', away_team, ' - ', date_event),
    # )
    event_location: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
