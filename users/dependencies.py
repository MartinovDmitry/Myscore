from datetime import datetime

from fastapi import HTTPException, status, Depends
from fastapi.requests import Request
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db_helper import session_factory
from users.dao import UserDAO


def get_access_token(request: Request) -> str:
    """
    This func is getting access (jwt) token from request
    """
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'Message': 'You are not authorized'},
        )
    return access_token


async def get_current_user(
        access_token: str = Depends(get_access_token),
):
    """
    This func is getting current user by payload from access (jwt) token
    """
    try:
        payload = jwt.decode(token=access_token, key=settings.JWT_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'Message': 'invalid token'}
        )
    expire: datetime = payload.get('exp')
    if (not expire) or (expire < datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'Message': 'Expire of token is over'}
        )
    user_id: int = int(payload.get('sub'))
    user = await UserDAO.find_one_or_none_with_context_manager(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'Message': 'Invalid access token'},
        )
    return user
