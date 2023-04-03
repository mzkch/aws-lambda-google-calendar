#!/bin/bash

# To be updated with the correct values!!
EXPECTED_ACCOUNT_ID="9999XXXXX000" # This is the AWS account ID for the expected environment
FUNCTION_NAME="arn:aws:lambda:ap-southeast-1:9999XXXXX000:function:aws-lambda-google-calendar"
ZIP_FILE="deployment.zip"

# Check if the AWS_DEFAULT_REGION environment variable is set
if [ -z "$AWS_DEFAULT_REGION" ]; then
    echo "AWS_DEFAULT_REGION is not set. Please set it to the AWS region where the Lambda function is located (e.g., 'ap-southeast-1')."
    exit 1
fi

# Check if the AWS_SECRET_ACCESS_KEY environment variable is set
if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "AWS_SECRET_ACCESS_KEY is not set. Please set it to the secret access key for the AWS account."
    exit 1
fi

# Check if the AWS_ACCESS_KEY_ID environment variable is set
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "AWS_ACCESS_KEY_ID is not set. Please set it to the access key ID for the AWS account."
    exit 1
fi

# Check if the current AWS account is the expected account
CURRENT_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
if [ "$CURRENT_ACCOUNT_ID" != "$EXPECTED_ACCOUNT_ID" ]; then
    echo "Current AWS account '$CURRENT_ACCOUNT_ID' does not match expected account '$EXPECTED_ACCOUNT_ID'. Please switch to the correct AWS account."
    exit 1
fi

aws lambda update-function-code \
--function-name $FUNCTION_NAME \
--zip-file fileb://$ZIP_FILE

echo "Uploaded $ZIP_FILE to $FUNCTION_NAME"
