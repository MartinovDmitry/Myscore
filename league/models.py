from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class League(Base):
    __tablename__ = 'leagues'

    league_name: Mapped[str]
    country: Mapped[str]
    clubs_number: Mapped[int]
    club_id: Mapped[int] = mapped_column(ForeignKey('clubs.id'))
