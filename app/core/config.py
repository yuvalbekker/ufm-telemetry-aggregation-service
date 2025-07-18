import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "UFM Telemetry Aggregation Service"
    API_V1_STR: str = "/telemetry"

    # Health api
    SERVICE_NAME: str = "ufm-telemetry-aggregation-service"
    HEALTHY_STATUS: str = "OK"
    SERVICE_VERSION: str = "REPLACE_ME"

    # Configuration
    SQS_QUEUE_URL: str = os.environ.get("SQS_QUEUE_URL", "http://localhost:4566/000000000000/ufm-telemetry-aggregation-sqs")
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    SQS_ENDPOINT_URL: str = os.environ.get("SQS_ENDPOINT_URL", "http://localhost:4566")
    DB_URL: str = os.environ.get("DB_URL", "postgresql+psycopg2://user:password1@localhost:5432/telemetry_aggregation_db")


    class Config:
        env_file = ".env"

settings = Settings()