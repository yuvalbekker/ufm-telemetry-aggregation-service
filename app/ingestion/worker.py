import time
import boto3
import app.db.utils as db_utils
from app.core.config import settings
from handler import process_message

# SQS Client
sqs = boto3.client(
    "sqs",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.SQS_ENDPOINT_URL,
)

def main():
    engine = db_utils.get_engine(settings.DB_URL)
    SessionLocal = db_utils.get_session_maker(engine)
    db_utils.ensure_tables(engine)

    print("Starting SQS worker...")
    while True:
        response = sqs.receive_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
        )
        messages = response.get("Messages", [])
        if not messages:
            print("No messages received")
            time.sleep(2)
            continue
        for msg in messages:
            try:
                process_message(msg["Body"], SessionLocal)
                sqs.delete_message(
                    QueueUrl=settings.SQS_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"Error processing message, will return to queue: {e}")
                # No delete_message call here: message will become visible again after visibility timeout

if __name__ == "__main__":
    main()
