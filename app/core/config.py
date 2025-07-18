from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "UFM Telemetry Aggregation Service"
    API_V1_STR: str = "/api/v1"

    # Health api
    SERVICE_NAME: str = "ufm-telemetry-aggregation-service"
    HEALTHY_STATUS: str = "OK"
    SERVICE_VERSION: str = "REPLACE_ME"

    class Config:
        env_file = ".env"

settings = Settings()