import json
from app.schemas.metric import SwitchMetric
from app.models.metric import Metric
import app.db.utils as db_utils

def process_message(message_body, SessionLocal):
    try:
        # Step 1: Parse the SNS notification envelope
        sns_envelope = json.loads(message_body)
        # Step 2: Extract and parse the actual metrics list from the "Message" field
        metrics = json.loads(sns_envelope["Message"])
        db_metrics = []
        for metric_dict in metrics:
            # Validate/parse using Pydantic, then save as SQLAlchemy
            metric = SwitchMetric(**metric_dict)
            db_metric = Metric(
                switch_id=metric.switch_id,
                bandwidth_usage=metric.bandwidth_usage,
                latency=metric.latency,
                packet_errors=metric.packet_errors,
                collection_time=metric.collection_time,
                # timestamp will be set by DB default
            )
            db_metrics.append(db_metric)
        with SessionLocal() as session:
            db_utils.upsert_metrics(session, db_metrics)
        print(f"Inserted {len(metrics)} metrics into the DB.")
    except Exception as e:
        print("Error processing message:", e)
