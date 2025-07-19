from fastapi import APIRouter
from fastapi.responses import FileResponse
from typing import Any

from counters.schemas.health import Health
from counters.schemas.error_responses import HEALTH_ERROR_RESPONSES
from counters.resources.generate_counters import generate_csv
from counters.core.config import settings

router = APIRouter()


@router.get("", response_model=Health, responses=HEALTH_ERROR_RESPONSES)
def counters() -> Any:
    generate_csv(settings.CSV_PATH, settings.NUMBER_OF_TELEMETRY_SWITCHES)

    # Return CSV as file response
    return FileResponse(settings.CSV_PATH, media_type="text/csv", filename="telemetry_sample.csv")
