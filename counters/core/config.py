import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "UFM Telemetry Counters Service"
    API_V1_STR: str = ""

    # Health api
    SERVICE_NAME: str = "ufm-counters-service"
    HEALTHY_STATUS: str = "OK"
    SERVICE_VERSION: str = "1.0.0"

    NUMBER_OF_TELEMETRY_SWITCHES: int = 100
    CSV_PATH: str = "telemetry_sample.csv"

    class Config:
        env_file = ".env"

settings = Settings()