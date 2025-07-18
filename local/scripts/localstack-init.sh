#!/bin/bash
set -e

echo "Initializing localstack resources..."
TOPIC_ARN=$(awslocal sns create-topic --name ufm-telemetry-aggregation-sns --query 'TopicArn' --output text)
QUEUE_URL=$(awslocal sqs create-queue --queue-name ufm-telemetry-aggregation-sqs --query 'QueueUrl' --output text)
QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url "$QUEUE_URL" --attribute-name QueueArn --query 'Attributes.QueueArn' --output text)

awslocal sns subscribe \
    --topic-arn "$TOPIC_ARN" \
    --protocol sqs \
    --notification-endpoint "$QUEUE_ARN"

echo "SNS topic, SQS queue, and subscription created!"