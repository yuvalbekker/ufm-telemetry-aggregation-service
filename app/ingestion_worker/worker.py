import os
import json
import time
import boto3
from app.schemas.metric import SwitchMetric
from app.models.metric import Metric
import app.db.utils as db_utils

# Configuration
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "http://localhost:4566/000000000000/ufm-telemetry-aggregation-sqs")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SQS_ENDPOINT_URL = os.environ.get("SQS_ENDPOINT_URL", "http://localhost:4566")
DB_URL = os.environ.get("DB_URL", "postgresql+psycopg2://user:pass@localhost:5432/telemety_aggregation_db")

# SQS Client
sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION,
    endpoint_url=SQS_ENDPOINT_URL,
)

# DB Utils
engine = db_utils.get_engine(DB_URL)
SessionLocal = db_utils.get_session_maker(engine)
db_utils.ensure_tables(engine)

def process_message(message_body):
    try:
        metrics = json.loads(message_body)
        db_metrics = []
        for metric_dict in metrics:
            # Validate/parse using Pydantic, then save as SQLAlchemy
            metric = SwitchMetric(**metric_dict)
            db_metric = Metric(
                switch_id=metric.switch_id,
                bandwidth_usage=metric.bandwidth_usage,
                latency=metric.latency,
                packet_errors=metric.packet_errors,
                collectionTime=metric.collectionTime,
                # timestamp will be set by DB default
            )
            db_metrics.append(db_metric)
        with SessionLocal() as session:
            db_utils.upsert_metrics(session, db_metrics)
        print(f"Inserted {len(metrics)} metrics into the DB.")
    except Exception as e:
        print("Error processing message:", e)

def main():
    print("Starting SQS worker...")
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
        )
        messages = response.get("Messages", [])
        if not messages:
            print("No messages received")
            time.sleep(2)
            continue
        for msg in messages:
            process_message(msg["Body"])
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

if __name__ == "__main__":
    main()
