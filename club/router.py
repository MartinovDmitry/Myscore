from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from club.dao import ClubDAO
from club.schemas import SchClubCreate, SchClubResponse
from club.view import get_club_by_title_view, create_club_view
from db_helper import session_factory
from permission import permission

router = APIRouter(
    prefix='/clubs',
    tags=['Clubs'],
)


@router.get('/{title}')
async def get_club_by_title(
        title: str,
        session: AsyncSession = Depends(session_factory),
) -> SchClubResponse:
    club = await get_club_by_title_view(
        title=title,
        session=session,
    )
    return club


@router.post('/')
async def create_club(
        club: SchClubCreate,
        role: str = Depends(permission.check_role_admin_of_user),
        session: AsyncSession = Depends(session_factory),
):
    await create_club_view(
        club=club,
        session=session,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'Message': f'Club {club.title} is created'}
    )
