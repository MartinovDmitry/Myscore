from datetime import datetime

from fastapi import HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from exceptions import UserAlreadyExistsException
from users.auth import authenticate_user, token, get_password_hash
from users.dao import TokenDAO, UserDAO
from users.models import User
from users.schemas import SchUserRegister
from users.schemas_token import TokenResponse


async def register_user_view(
        user_data: SchUserRegister,
        session: AsyncSession,
):
    existing_user = await UserDAO.find_one_or_none(
        username=user_data.username,
        session=session,
    )
    if existing_user:
        raise UserAlreadyExistsException
    await UserDAO.create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        session=session,
    )
    return JSONResponse(
        content={'Message': f'User with email: {user_data.email} is created'}
    )


async def login_user_view(
        form_data: OAuth2PasswordRequestForm,
        response: Response,
        session: AsyncSession,
) -> TokenResponse:
    user = await authenticate_user(
        username=form_data.username,
        plain_password=form_data.password,
        session=session,
    )
    couple_token = token.get_user_token({'sub': str(user.id)})
    await TokenDAO.check_count_of_max_report(
        user_id=user.id,
        session=session,
    )
    await TokenDAO.create_token_record_in_db(
        refresh_token=couple_token.refresh_token,
        user_id=user.id,
        session=session,
    )
    await UserDAO.verify_user(
        user_id=user.id,
        session=session,
        is_verified=True,
        verified_at=datetime.utcnow(),
    )
    response.set_cookie('refresh_token', couple_token.refresh_token, httponly=True, max_age=settings.JWT_EXPIRE)
    response.set_cookie('access_token', couple_token.access_token, httponly=True)
    return couple_token


async def logout_user_view(response: Response, request: Request, session: AsyncSession):
    # Get refresh_token
    refresh_token = request.cookies.get('refresh_token')
    # Get payload from refresh_token (user_id)
    payload = await token.get_payload_from_refresh_token(refresh_token=refresh_token, session=session)
    # Delete records in db's table refreshtokens
    await TokenDAO.delete_token_records_in_db(user_id=payload.user_id, session=session)
    # Delete cookies
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')


async def refresh_access_token_view(
        refresh_token: str,
        session: AsyncSession,
) -> TokenResponse:
    user: User = await token.get_user_by_refresh_token(
        refresh_token=refresh_token,
        session=session,
    )
    couple_token = token.get_user_token({'sub': user.id})
    await TokenDAO.update_refresh_token(
        user_id=user.id,
        refresh_token=couple_token.refresh_token,
        session=session,
    )
    return couple_token
