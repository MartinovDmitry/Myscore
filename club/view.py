from sqlalchemy.ext.asyncio import AsyncSession

from club.dao import ClubDAO
from club.schemas import SchClubCreate


async def create_club_view(
        club: SchClubCreate,
        session: AsyncSession,
):
    await ClubDAO.create_club(
        club=club,
        session=session,
    )


async def get_club_by_title_view(
        title: str,
        session: AsyncSession,
):
    result = await ClubDAO.get_club_by_title(
        title=title,
        session=session,
    )
    club = result.scalar_one_or_none()
    return club
