import time

from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
# from logger_file import logger

# logger.info('Middleware is working',)


class MeasureTime(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        print(process_time)
        return response


