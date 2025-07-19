import time
from app.core.config import settings
from app.ingestion.handler import process_message
import app.db.utils as db_utils
from app.aws.utils import get_sqs_client, receive_messages, delete_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_session():
    engine = db_utils.get_engine(settings.DB_URL)
    SessionLocal = db_utils.get_session_maker(engine)
    db_utils.ensure_tables(engine)
    return SessionLocal

def main():
    # Prepare the session maker once on worker startup
    SessionLocal = get_session()
    sqs = get_sqs_client()

    logger.info("Starting SQS worker...")
    while True:
        messages = receive_messages(sqs, settings.SQS_QUEUE_URL, settings.MAX_MESSAGES_RECEIVED, settings.WAIT_TIME)
        if not messages:
            logger.info("No messages received")
            time.sleep(5)
            continue
        for msg in messages:
            try:
                with SessionLocal() as session:
                    process_message(msg["Body"], session)
                delete_message(sqs, settings.SQS_QUEUE_URL, msg["ReceiptHandle"])
                logger.info("Successfully processed and deleted message with ReceiptHandle: %s", msg["ReceiptHandle"])
            except Exception as e:
                logger.error(
                    "Error processing message (ReceiptHandle: %s), will return to queue after visibility timeout: %s",
                    msg.get("ReceiptHandle", "UNKNOWN"),
                    e,
                    exc_info=True
                )

if __name__ == "__main__":
    main()
