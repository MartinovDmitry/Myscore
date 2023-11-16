import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from users.router import router as users_router

app = FastAPI()
app.include_router(users_router)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'Message': exc.errors()}),
    )

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
