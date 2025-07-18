import os
import json
import time
import random
import uuid
from datetime import datetime, timezone
import boto3
from app.schemas.metric import SwitchMetric

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:000000000000:ufm-telemetry-aggregation-sns')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SNS_ENDPOINT_URL = os.environ.get('SNS_ENDPOINT_URL', 'http://localhost:4566')

sns = boto3.client(
    'sns',
    region_name=AWS_REGION,
    endpoint_url=SNS_ENDPOINT_URL
)

def generate_metric() -> SwitchMetric:
    """Generate a SwitchMetric without the timestamp (to be set by DB)."""
    return SwitchMetric(
        switch_id=str(uuid.uuid4()),
        bandwidth_usage=round(random.uniform(10, 1000), 2),
        latency=round(random.uniform(0.1, 10.0), 3),
        packet_errors=random.randint(0, 100),
        collection_time=datetime.now(timezone.utc)
    )

def main():
    print("Starting event generator (timestamp excluded; will be set in DB)")
    while True:
        num_events: int = random.randint(2, 10)
        events: list[SwitchMetric]= [generate_metric() for _ in range(num_events)]
        # Exclude the timestamp field when serializing
        message: str = json.dumps([event.model_dump(exclude={"timestamp"}) for event in events], default=str)
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message
        )
        print(f"Published {num_events} events: {message}")
        print("Sleeping for 10 seconds...\n")
        time.sleep(10)

if __name__ == "__main__":
    main()