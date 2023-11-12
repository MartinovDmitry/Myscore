import uuid
from base64 import b64encode
from datetime import datetime, timedelta
from secrets import token_bytes
from jose import jwt, JWTError

from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from users.dao import UserDAO
from users.models import RefreshToken, User
from users.schemas_token import TokenResponse

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def secret_key():
    return b64encode(token_bytes(32)).decode()


class Token:
    expire = settings.JWT_EXPIRE

    @staticmethod
    def create_access_token(data: dict, expire: int = expire) -> str:
        """
        This func is creating access (jwt) token
        """
        payload = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expire)
        payload.update({'exp': expire})
        encode_jwt_access = jwt.encode(
            payload, key=settings.JWT_KEY, algorithm=settings.ALGORITHM,
        )
        return encode_jwt_access

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        This func is creating refresh (uuid4) token
        """
        refresh_token = RefreshToken(
            refresh_token=str(uuid.uuid4()),
            user_id=data['sub'],
        )
        return refresh_token.refresh_token

    @classmethod
    def get_user_token(cls, data: dict) -> TokenResponse:
        """
        This func is uniting access (jwt) and refresh (uuid4) tokens
        """
        access_token = cls.create_access_token(data=data)
        refresh_token = cls.create_refresh_token(data=data)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    async def get_payload_from_refresh_token(refresh_token: str, session: AsyncSession) -> RefreshToken:
        """
        This func is returning payload from refresh (uuid4) token
        """
        query = select(RefreshToken).filter_by(refresh_token=refresh_token)
        payload = await session.execute(query)
        payload = payload.scalar_one_or_none()
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={'Message': 'Refresh token is invalid'},
                headers={'WWW-Authenticate': 'Bearer'}
            )
        return payload

    @classmethod
    async def get_user_by_refresh_token(cls, refresh_token: str, session: AsyncSession) -> User:
        """
        This func is returning user by payload of refresh (uuid4) tokens
        """
        payload: RefreshToken = await cls.get_payload_from_refresh_token(refresh_token=refresh_token, session=session)
        user_id: int = payload.user_id
        user = await UserDAO.find_one_or_none(id=user_id, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={'Message': 'Invalid refresh token'}
            )
        return user


token = Token()


async def authenticate_user(
        username: str,
        plain_password: str,
        session: AsyncSession,
):
    existing_user = await UserDAO.find_one_or_none(
        username=username,
        session=session,
    )
    if existing_user is None or not verify_password(plain_password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'Message': 'Authentication error'}
        )
    return existing_user
