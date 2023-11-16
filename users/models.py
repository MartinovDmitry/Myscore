import uuid
from datetime import datetime, timedelta
from enum import Enum

from pydantic import EmailStr
from sqlalchemy import String, text, ForeignKey, func, TIMESTAMP, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from config import settings
from db_helper import Base


class Role(Enum):
    CLIENT = 'CLIENT'
    ADMIN = 'ADMIN'
    SUPERADMIN = 'SUPERADMIN'


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[EmailStr] = mapped_column(String, unique=True)
    role: Mapped[Role] = mapped_column(default=Role.CLIENT)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    verified_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )


# time = datetime.utcnow() + timedelta(settings.REFR_EXPIRE)


class RefreshToken(Base):
    __tablename__ = 'refreshtokens'

    refresh_token: Mapped[uuid.uuid4()] = mapped_column(String, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    expire_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow() + timedelta(settings.REFR_EXPIRE),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
