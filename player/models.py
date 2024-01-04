from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class Player(Base):
    __tablename__ = 'players'

    first_name: Mapped[str]
    second_name: Mapped[str]
    age: Mapped[int]
    club_id: Mapped[int] = mapped_column(ForeignKey('clubs.id'))
    matches: Mapped[int]
    goals: Mapped[int]
    assists: Mapped[int]
    yellow_cards: Mapped[int]
    red_cards: Mapped[int]
    trophies_num: Mapped[int]
    rating: Mapped[int] = mapped_column(nullable=False)
