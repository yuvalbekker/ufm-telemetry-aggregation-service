import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Service
    PROJECT_NAME: str = "UFM Telemetry Aggregation Service"
    API_V1_STR: str = "/telemetry"

    # Health api
    SERVICE_NAME: str = "ufm-telemetry-aggregation-service"
    HEALTHY_STATUS: str = "OK"
    SERVICE_VERSION: str = "1.0.0"

    #StatsD
    GRAPHITE_HOST: str = "graphite"

    # DB
    DB_URL: str = os.environ.get("DB_URL", "postgresql+psycopg2://user:password1@localhost:5432/telemetry_aggregation_db")

    # SQS
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    MAX_MESSAGES_RECEIVED: int = os.environ.get("MAX_MESSAGES_RECEIVED", 10)
    WAIT_TIME: int = os.environ.get("WAIT_TIME", 5)
    SQS_QUEUE_URL: str = os.environ.get("SQS_QUEUE_URL", "http://localstack:4566/000000000000/ufm-telemetry-aggregation-sqs")
    SQS_ENDPOINT_URL: str = os.environ.get("SQS_ENDPOINT_URL", "http://localhost:4566")


    class Config:
        env_file = ".env"

settings = Settings()