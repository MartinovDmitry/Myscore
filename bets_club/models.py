from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, MappedColumn

from db_helper import Base


class PremierLeagueClub(Base):
    __tablename__ = 'premier_league_clubs'

    name: Mapped[str]
    abbreviation: Mapped[str]
    record: Mapped[str] = mapped_column(String())

