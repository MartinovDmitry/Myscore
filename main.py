import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import settings
from redis_tools import RedisTools
from users.router import router as users_router
from player.router import router as player_router
from league.router import router as league_router
from club.router import router as club_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = RedisTools.async_redis
    # redis = aioredis.from_url(url=settings.redis_url, encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='redis-cache')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(player_router)
app.include_router(league_router)
app.include_router(club_router)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'Message': exc.errors()}),
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
