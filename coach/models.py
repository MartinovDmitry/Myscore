from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class Coach(Base):
    __tablename__ = 'coaches'

    first_name: Mapped[str]
    second_name: Mapped[str]
    age: Mapped[int]
    country_birth: Mapped[str]
    earlier_clubs = Mapped[list[str]]
    current_club: Mapped[str]
    club_id: Mapped[int] = mapped_column(ForeignKey('clubs.id'))
    salary: Mapped[int]
