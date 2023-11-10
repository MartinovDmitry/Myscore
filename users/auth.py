from base64 import b64encode
from datetime import datetime, timedelta
from secrets import token_bytes
from jose import jwt

from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from users.dao import UserDAO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload.update({'exp': expire})
    encode_jwt = jwt.encode(
        payload, key=settings.JWT_KEY, algorithm=settings.ALGORITHM,
    )
    return encode_jwt


def secret_key():
    return b64encode(token_bytes(32)).decode()


async def authenticate_user(
        email: EmailStr,
        plain_password: str,
        session: AsyncSession,
):
    existing_user = await UserDAO.find_one_or_none(
        email=email,
        session=session,
    )
    if not existing_user or not verify_password(plain_password, existing_user.hashed_password):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'Message': 'Authentication error'}
        )
    return existing_user
