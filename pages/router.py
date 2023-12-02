from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from league.router import get_league_by_title

router = APIRouter(
    prefix='/pages',
    tags=['Frontend'],
)
templates = Jinja2Templates(
    directory='templates'
)


@router.get('/leagues')
async def get_league_page(
        request: Request,
        leagues=Depends(get_league_by_title),
):
    return templates.TemplateResponse(
        name='leagues.html',
        context={
            'request': request,
            'leagues': leagues,
        },
    )
