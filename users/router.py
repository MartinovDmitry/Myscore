from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db_helper import session_factory
from users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from users.dao import UserDAO
from users.schemas import SchUserRegister, SchUserBase, SchUserLogin

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register', response_model=SchUserBase)
async def register_user(
        user_data: SchUserRegister,
        session: AsyncSession = Depends(session_factory)
):
    existing_user = await UserDAO.find_one_or_none(
        email=user_data.email,
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
        user_data: SchUserLogin,
        response: Response,
        session: AsyncSession = Depends(session_factory),
):
    user = await authenticate_user(
        email=user_data.email,
        plain_password=user_data.password,
        session=session,
    )
    access_token = create_access_token({'sub': user.id})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'access_token': access_token}

