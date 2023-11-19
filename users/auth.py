import uuid
from base64 import b64encode
from datetime import datetime, timedelta
from secrets import token_bytes
from typing import NoReturn

from jose import jwt

from fastapi.responses import Response
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from exceptions import WrongUserCredentialsException, InvalidRefreshTokenException, InvalidRefreshTokenExpireException
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
            raise InvalidRefreshTokenException
        return payload

    @classmethod
    async def get_user_by_refresh_token(cls, refresh_token: str, session: AsyncSession) -> User:
        """
        This func is returning user by payload of refresh (uuid4) tokens
        """
        payload: RefreshToken = await cls.get_payload_from_refresh_token(refresh_token=refresh_token, session=session)
        if payload.expire_at < datetime.utcnow():
            raise InvalidRefreshTokenExpireException
        user_id: int = payload.user_id
        user = await UserDAO.find_one_or_none(id=user_id, session=session)
        if not user:
            raise InvalidRefreshTokenException
        return user


token = Token()


class Cookie:
    @staticmethod
    def set_cookies(couple_token: TokenResponse, response: Response) -> NoReturn:
        response.set_cookie('refresh_token', couple_token.refresh_token, httponly=True, max_age=settings.JWT_EXPIRE)
        response.set_cookie('access_token', couple_token.access_token, httponly=True)

    @staticmethod
    def delete_cookies(response: Response):
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')


cookie = Cookie()


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
        raise WrongUserCredentialsException
    return existing_user
