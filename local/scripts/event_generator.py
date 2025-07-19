import os
import json
import csv
import requests
import logging
from typing import List
from datetime import datetime
import boto3
from app.schemas.metric import SwitchMetric
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:000000000000:ufm-telemetry-aggregation-sns')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SNS_ENDPOINT_URL = os.environ.get('SNS_ENDPOINT_URL', 'http://localhost:4566')
COUNTERS_API_URL = os.environ.get('COUNTERS_API_URL', 'http://localhost:9001/counters')
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', 10))

sns = boto3.client(
    'sns',
    region_name=AWS_REGION,
    endpoint_url=SNS_ENDPOINT_URL
)

def fetch_counters_csv() -> List[SwitchMetric]:
    try:
        logger.info(f"Requesting telemetry from counters API: {COUNTERS_API_URL}")
        response = requests.get(COUNTERS_API_URL)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch data from counters API: {e}")
        raise

    decoded = response.content.decode('utf-8')
    reader = csv.DictReader(decoded.splitlines())
    metrics: List[SwitchMetric] = []
    for row in reader:
        try:
            # Convert string values to correct types if needed
            row['bandwidth_usage'] = float(row['bandwidth_usage'])
            row['latency'] = float(row['latency'])
            row['packet_errors'] = int(row['packet_errors'])
            # Parse collection_time as datetime if needed
            if isinstance(row['collection_time'], str):
                row['collection_time'] = datetime.fromisoformat(row['collection_time'].replace('Z', '+00:00'))
            metrics.append(SwitchMetric(**row))
        except Exception as e:
            logger.error(f"Failed to parse row {row}: {e}")
    logger.info(f"Parsed {len(metrics)} metric rows from CSV")
    return metrics

def main() -> None:
    logger.info("Starting continuous telemetry fetch/send loop...")
    while True:
        logger.info("Fetching telemetry from counters API...")
        metrics: List[SwitchMetric] = fetch_counters_csv()
        logger.info(f"Fetched {len(metrics)} metrics from counters API.")

        # Send in batches
        for i in range(0, len(metrics), BATCH_SIZE):
            batch = metrics[i:i+BATCH_SIZE]
            message = json.dumps([m.model_dump(exclude={"timestamp"}) for m in batch], default=str)
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message
                )
                logger.info(f"Published batch {i//BATCH_SIZE+1} ({len(batch)} events) to SNS.")
            except Exception as e:
                logger.error(f"Failed to publish batch {i//BATCH_SIZE+1}: {e}")
            if i + BATCH_SIZE < len(metrics):
                logger.info("Sleeping for 10 seconds before sending next batch...")
                time.sleep(10)
        # After sending all metrics, loop and fetch again

if __name__ == "__main__":
    main()
