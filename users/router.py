import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db_helper import session_factory
from users.auth import get_password_hash, authenticate_user, token
from users.dao import UserDAO, TokenDAO
from users.models import User
from users.schemas import SchUserRegister, SchUserBase, SchUserLogin

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)
auth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/login')


@router.post('/register', response_model=SchUserBase)
async def register_user(
        user_data: SchUserRegister,
        session: AsyncSession = Depends(session_factory)
):
    existing_user = await UserDAO.find_one_or_none(
        username=user_data.username,
        session=session,
    )
    if existing_user:
        raise HTTPException(
            status_code=500,
        )
    await UserDAO.create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        session=session,
    )
    return JSONResponse(
        content={'Message': f'User with email: {user_data.email} is created'}
    )


@router.post('/login')
async def login_user(
        # user_data: SchUserLogin,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
        session: AsyncSession = Depends(session_factory),
):
    """
    Function's duties:
    1) Checking existing user and validation user's credentials
    2) Creating a couple of tokens: access (jwt) anf refresh (uuid4) tokens
    3) Adding refresh token in database
    4) Setting refresh token in cookie
    5) Returning a couple of tokens and additional info
    """
    user = await authenticate_user(
        username=form_data.username,
        plain_password=form_data.password,
        session=session,
    )
    couple_token = token.get_user_token({'sub': user.id})
    await TokenDAO.create_token(
        refresh_token=couple_token.refresh_token,
        user_id=user.id,
        session=session,
    )
    response.set_cookie('refresh_token', couple_token.refresh_token, httponly=True)
    return {'token_response': couple_token}


@router.post('/refresh')
async def refresh_access_token(
        refresh_token: str = Header(),
        session: AsyncSession = Depends(session_factory),
):
    """
    Function's duties:
    1) Getting payload (line from refreshtokens table) from refresh (uuid4) token and getting the user
    2) Creating a new couple of tokens: access (jwt) and refresh (uuid4) tokens
    3) Updating refresh (uuid4) token in database
    """
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
    return {'token_response': couple_token}
