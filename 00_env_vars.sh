#!/bin/bash
# This is the global environment file
# for our Polly demo

# USE Absolute path for PROJECT DIR
export PROJECT_DIR='/home/ubuntu/aws-polly-demo-python'
export LOG_DIR='logs'
export LOG_FILE='app-deployment.log'

# dynamodb vars
export REGION='us-east-1'
export TABLE_NAME='AnhPollyProject'

#S3
export BUCKET_IN='anh-pollybucket-in'
export BUCKET_OUT='anh-pollybucket-out'

#SNS
export TOPIC_NAME='anh_polly_events'

#IAM
export LAMBDA_POLICY='anh-lambda-policy'
export LAMBDA_ROLE='anh-lambda-role'

#API GATEWAY
export API_NAME='ServerLessPollyAPI'
export API_STAGE_NAME='development'




