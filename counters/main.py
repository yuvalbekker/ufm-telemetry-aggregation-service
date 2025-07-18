from fastapi import FastAPI
from counters.api.api_v1.api import api_router
from counters.core.config import settings

counters = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
counters.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:counters", host="127.0.0.1", port=9001, reload=True)
