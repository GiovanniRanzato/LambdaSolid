#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Variables
ENDPOINT_URL=http://localhost:4566

#Create SNS
docker exec -it localstack awslocal sns create-topic --name "$SNS_SAMPLE_TOPIC" --endpoint-url "$LOCALSTACK_ENDPOINT_URL" --region "$SNS_REGION"

# Create S3 Bucket
# docker exec -it localstack awslocal s3api create-bucket --bucket "$S3_SAMPLE_BUCKET" --endpoint-url "$LOCALSTACK_ENDPOINT_URL"

# Copy the file to the Docker container
# docker cp ./tests/helper/files/test_object.txt localstack:/tmp/test_object.txt
# Put file into S3 bucket
# docker exec -it localstack awslocal s3api put-object --bucket "$S3_SAMPLE_BUCKET" --key "test_object_content.txt" --body /tmp/test_object.txt --endpoint-url "$LOCALSTACK_ENDPOINT_URL"

docker exec -it localstack awslocal dynamodb create-table \
  --table-name "$DYNAMODB_SAMPLE_TABLE" \
  --attribute-definitions \
      AttributeName="$DYNAMODB_SAMPLE_TABLE_PK",AttributeType=S \
  --key-schema AttributeName="$DYNAMODB_SAMPLE_TABLE_PK",KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --endpoint-url "$LOCALSTACK_ENDPOINT_URL" \
  --region "$DYNAMODB_REGION"


# Create a secret in Secrets Manager
docker exec -it localstack awslocal secretsmanager create-secret \
  --name "$SECRETS_NAME" \
  --secret-string "{
    \"SAMPLE_SECRET\": \"$SAMPLE_SECRET\"
  }" \
  --endpoint-url "$LOCALSTACK_ENDPOINT_URL" \
  --region "$SECRETS_REGION"