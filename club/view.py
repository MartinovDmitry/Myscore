from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as, TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from club.dao import ClubDAO
from club.models import Club
from club.schemas import SchClubCreate, SchClubResponse
from exceptions import WrongCredentialsException
from tasks.celery_tasks import send_news


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
    club = await ClubDAO.get_club_by_title(
        title=title,
        session=session,
    )
    if club is None:
        raise WrongCredentialsException
    clubs_adapter = TypeAdapter(SchClubResponse)
    club_dict = clubs_adapter.validate_python(jsonable_encoder(club)).model_dump()
    send_news.delay(title=Club.__tablename__, content=club_dict, email_to='some_email')
    return club
