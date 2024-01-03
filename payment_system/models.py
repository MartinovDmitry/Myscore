from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import Base


class Payment(Base):
    __tablename__ = 'payments'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bonuses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    replenishment_at: Mapped[datetime] = mapped_column(default=None)
    withdrawal_at: Mapped[datetime] = mapped_column(default=None)

    __table_args__ = (
        CheckConstraint(count >= 0, name='check_count_positive')
    )
