from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder

from app.api.api_v1.api import api_router
from app.core.config import settings
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import time
from app.schemas.error_responses import Error
from typing import Callable, Dict
from app.common.observability.statsd import stats_client
import app.common.observability.metrics_names as mn
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)


@app.middleware("http")
async def send_call_metrics(request: Request, call_next: Callable) -> Dict:
    start_time = time.time()
    result = await call_next(request)

    api_endpoint = request.url.path.strip("/").replace("/", ".") or "root"
    status_code = result.status_code

    metric_name_count = mn.API_CALL_COUNT.format(api_endpoint=api_endpoint, status_code=status_code)
    metric_name_timing = mn.API_CALL_RUNTIME.format(api_endpoint=api_endpoint, status_code=status_code)

    diff = time.time() - start_time
    try:
        if stats_client:
            stats_client.incr(metric_name_count, count=1)
            stats_client.timing(metric_name_timing, delta=diff)
    except Exception as ex:
        logger.error(
            "Failed to send metrics to statsd. url: %s ,call runtime: %s: ,error: %s",
            request.url.path,
            diff,
            str(ex),
        )
    return result


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"general_exception_handler :: request:{str(request)}, exc:{str(exc)}")
    return JSONResponse(
        content=jsonable_encoder(Error(message=settings.INTERNAL_ERROR_MESSAGE)),
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
