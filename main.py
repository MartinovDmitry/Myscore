import time

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from middleware import MeasureTime
from redis_tools import RedisTools
from users.router import router as users_router
from player.router import router as player_router
from league.router import router as league_router
from club.router import router as club_router

from pages.router import router as pages_router
from images.router import router as images_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = RedisTools.async_redis
    # redis = aioredis.from_url(url=settings.redis_url, encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='redis-cache')
    yield


app = FastAPI(lifespan=lifespan)

app.mount(path='/static', app=StaticFiles(directory='static'), name='static')

app.include_router(users_router)
app.include_router(player_router)
app.include_router(league_router)
app.include_router(club_router)

app.include_router(pages_router)
app.include_router(images_router)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'Message': exc.errors()}),
    )

#######################################
# MiddleWare ##########################
#######################################
app.add_middleware(MeasureTime)


####################################################
# CORS #############################################
####################################################

origins = [
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin', 'Authorization'
    ],
)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
