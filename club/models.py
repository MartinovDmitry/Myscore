from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class Club(Base):
    __tablename__ = 'clubs'

    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    date_of_foundation: Mapped[date]
    location: Mapped[str]
    players_quantity: Mapped[int]
    stuff_quantity: Mapped[int]
    coach_name: Mapped[str]
    league_name: Mapped[str]
