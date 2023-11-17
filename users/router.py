from typing import Annotated

from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from redis_tools import redis_tools
from users.dependencies import get_current_user
from users.models import User
from users.schemas import SchUserRegister, SchUserBase
from users.schemas_token import TokenResponse
from users.view import login_user_view, refresh_access_token_view, register_user_view, logout_user_view

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)
auth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/login')


@router.post('/register', response_model=SchUserBase)
async def register_user(
        user_data: SchUserRegister,
        session: AsyncSession = Depends(session_factory)
) -> JSONResponse:
    """
    Function's duties:
    1) Finding user in database (if user exists - error)
    2) Creating user in database
    3) Returning JSONResponse with info
    """
    response = await register_user_view(
        user_data=user_data,
        session=session,
    )
    return response


@router.post('/login')
async def login_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
        session: AsyncSession = Depends(session_factory),
) -> TokenResponse:
    """
    Function's duties:
    1) Checking existing user and validation user's credentials
    2) Creating a couple of tokens: access (jwt) anf refresh (uuid4) tokens
    3) Checking count of refreshtokens records in db, should be less than 3
    4) Adding refresh token in database
    5) Setting refresh token in cookie
    6) Updating user in database: is_verified, verified_at
    7) Returning a couple of tokens and additional info
    """
    couple_token = await login_user_view(
        form_data=form_data,
        response=response,
        session=session,
    )
    return couple_token


@router.post('/logout')
async def logout_user(
        response: Response,
        request: Request,
        session: AsyncSession = Depends(session_factory),
):
    """
    Function's duties:
    1) Getting refresh_token
    2) Getting payload from refresh_token (user_id)
    3) Deleting records in db's table refreshtokens
    4) Deleting cookies
    """
    await logout_user_view(response=response, request=request, session=session)
    return {'Message': 'User logout'}


@router.post('/refresh')
async def refresh_access_token(
        refresh_token: str = Header(),
        session: AsyncSession = Depends(session_factory),
) -> TokenResponse:
    """
    Function's duties:
    1) Getting payload (line from refreshtokens table) from refresh (uuid4) token and getting the user
    2) Creating a new couple of tokens: access (jwt) and refresh (uuid4) tokens
    3) Updating refresh (uuid4) token in database
    """
    couple_token = await refresh_access_token_view(
        refresh_token=refresh_token,
        session=session,
    )
    return couple_token


@router.get('/current_user')
async def get_current_user(
        user: User = Depends(get_current_user),
) -> SchUserBase:
    """
    Function's duties:
    1) Getting access token from request
    2) Checking payload of access token
    3) Returning current user by access token
    """
    return user


@router.post('/')
async def example(request: Request):
    ref_token = request.cookies.get('refresh_token')
    print(ref_token)
    redis_tools.set_pair('refresh_token', ref_token)
    res = redis_tools.get_pair('refresh_token')
    print(res)
