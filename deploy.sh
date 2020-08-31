#!/bin/bash
# Deploy the stack
echo "Reading in env variables.."
source ./00_env_vars.sh
echo "Creating dynamodb tables.."
python3 ./01_create_dynamodb_table.py
echo "Creating S3 Buckets.."
python3 ./02_create_s3_buckets.py
echo "Creating SNS Topic.."
python3 ./03_create_sns_topic.py
sleep 10
check=`aws sns list-topics|grep -i $TOPIC_NAME|wc -l`
if [ $check -eq 0 ]
then
	echo "Exiting. Check the error logs. Could not create topic"
	exit 1
else
	echo "SNS Topic created"
fi
echo "Creating IAM policies.."
python3 ./04_create_iam_policy_roles.py
sleep 10
check=`aws iam list-policies|grep PolicyName|grep -i "$LAMBDA_POLICY" |wc -l`
check2=`aws iam list-roles|grep RoleName|grep -i "$LAMBDA_ROLE"|wc -l`
if [ $check -eq 0 ] || [ $check2 -eq 0 ]
then
	echo "Exiting. IAM Role creation failed. Check logs"
	exit 1
else
	echo "IAM Role created"
fi
echo "Creating lambda POST function.."
python3 ./05_create_newpostreader_lambda.py
sleep 10
check=`aws lambda list-functions|grep  FunctionName | tr '\012' ' '|grep -i PostReader_NewPosts|wc -l`
if [ $check -eq 0 ]
then
	echo "Exiting. Check the error logs. Could not create topic"
	exit 1
else
	echo "Lambda function has been created"
fi

echo "Creating polly text to mp3 lambda function.."
python3 ./06_create_convert_audio.py
sleep 10
check=`aws lambda list-functions|grep  FunctionName | tr '\012' ' '|grep -i PostReader_ConvertToAudio|wc -l`
if [ $check -eq 0 ]
then
	echo "Exiting. Check the error logs. Could not create topic"
	exit 1
else
	echo "Lambda function has been created"
fi

echo "Creating lambda GET function.."
python3 ./07_create_getposts_function.py
sleep 10
check=`aws lambda list-functions|grep  FunctionName | tr '\012' ' '|grep -i PostReader_GetPosts|wc -l`
if [ $check -eq 0 ]
then
	echo "Exiting. Check the error logs. Could not create topic"
	exit 1
else
	echo "Lambda function has been created"
fi
echo "Adding SNS Triggers to Lambda.."
python3 ./08_add_sns_trigger_to_lambda.py
sleep 10
check=`aws sns list-subscriptions |grep TopicArn|grep "$TOPIC_NAME"|wc -l`
if [ $check -eq 0 ]
then
	echo "Exiting. Check the error logs. Could not create SNS Triggers"
	exit 1
else
	echo "SNS Trigger has been created"
fi

echo "Creating REST API Gateway components.."
cd ./apigw
python3 ./01-create-rest-api.py
echo "Creating API GET Method.."
sleep 10
check=`aws apigateway get-rest-apis|grep "$API_NAME"|wc -l`
if [ $check -eq 0 ]
then
	echo "Exiting. Check the error logs. Could not create REST API"
	exit 1
else
	echo "REST API has been created"
fi

python3 ./02-create-get-method.py
echo "Creating API POST Method.."
python3 ./03-create-post-method.py
echo "Creating API OPTIONS and CORS.."
python3 ./04-create-options-method.py
echo "Creating API Deployment.."
sleep 10
python3 ./05-create-deployment.py
sleep 10
echo "Adding Lambda permissions to API GW.."
python3 ./06-add-lambda-invocation-permission-apigw.py

cd ..
echo "Uploading website files to S3 bucket $BUCKET_IN"
python3 ./10_put_websitefiles_tobucket.py
echo "All Done. Please logon to AWS Console to validate stack"
echo "You can access the application at $BUCKET_IN.s3-website-us-east-1.amazonaws.com/index.html"
