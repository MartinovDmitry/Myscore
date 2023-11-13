from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class Club(Base):
    __tablename__ = 'clubs'

    title: Mapped[str]
    description: Mapped[Optional[str]]
    date_of_foundation: Mapped[date]
    location: Mapped[str]
    players_quantity: Mapped[int]
    stuff_quantity: Mapped[int]
    coach_name: Mapped[str]
    coach_id: Mapped[str] = mapped_column(ForeignKey('coaches.id'))
    league_name: Mapped[str]
    league_id: Mapped[int] = mapped_column(ForeignKey('leagues.id'))
