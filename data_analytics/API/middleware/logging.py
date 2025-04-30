import logging
from fastapi import Request, Response
import time

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"{request.method} {request.url.path} {response.status_code} {process_time:.2f}s")
    return response
