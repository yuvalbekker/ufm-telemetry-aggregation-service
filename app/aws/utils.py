import boto3
from app.core.config import settings

def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.SQS_ENDPOINT_URL,
    )

def receive_messages(sqs, queue_url: str, max_messages: int = 10, wait_time: int = 5):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time,
    )
    return response.get("Messages", [])

def delete_message(sqs, queue_url: str, receipt_handle: str):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
