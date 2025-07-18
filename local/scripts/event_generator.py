import os
import json
import csv
import requests
from typing import List
from datetime import datetime
import boto3
from app.schemas.metric import SwitchMetric
import time

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
    response = requests.get(COUNTERS_API_URL)
    response.raise_for_status()
    decoded = response.content.decode('utf-8')
    reader = csv.DictReader(decoded.splitlines())
    metrics: List[SwitchMetric] = []
    for row in reader:
        # Convert string values to correct types if needed
        row['bandwidth_usage'] = float(row['bandwidth_usage'])
        row['latency'] = float(row['latency'])
        row['packet_errors'] = int(row['packet_errors'])
        # Parse collection_time as datetime if needed
        if isinstance(row['collection_time'], str):
            row['collection_time'] = datetime.fromisoformat(row['collection_time'].replace('Z', '+00:00'))
        metrics.append(SwitchMetric(**row))
    return metrics


def main() -> None:
    print("Fetching telemetry from counters API...")
    metrics: List[SwitchMetric] = fetch_counters_csv()
    print(f"Fetched {len(metrics)} metrics from counters API.")

    # Send in batches
    for i in range(0, len(metrics), BATCH_SIZE):
        batch = metrics[i:i+BATCH_SIZE]
        message = json.dumps([m.model_dump(exclude={"timestamp"}) for m in batch], default=str)
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message
        )
        print(f"Published batch of {len(batch)} events to SNS.")
        if i + BATCH_SIZE < len(metrics):
            print("Sleeping for 10 seconds before sending next batch...\n")
            time.sleep(10)

if __name__ == "__main__":
    main()