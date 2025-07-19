import json
from app.schemas.metric import SwitchMetric
from app.models.metric import Metric
import app.db.utils as db_utils
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_message(message_body, session):
    sns_envelope = json.loads(message_body)
    metrics = json.loads(sns_envelope["Message"])
    db_metrics = []
    for metric_dict in metrics:
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
    db_utils.upsert_metrics(session, db_metrics)
    logger.info(f"Inserted {len(db_metrics)} metrics into the DB. Switch IDs: {[m.switch_id for m in db_metrics]}")
