#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('./lib')
import myutils
'''
  This function is triggered by SNS topic only and not via API GW
'''

iam = boto3.client('iam')
# sns = boto3.client('sns')
lambda_client = boto3.client('lambda')

function_name = 'PostReader_ConvertToAudio'

iam_role= os.environ.get('LAMBDA_ROLE', 'sk-lambda-role')
table_name=os.environ.get('TABLE_NAME','PollyProject')
bucket_out= os.environ.get('BUCKET_OUT','sk-pollybucket-out')

role_name = iam.get_role(RoleName=iam_role)
role_arn = role_name['Role']['Arn']
# topics = sns.list_topics()
# for topic in topics["Topics"]:
# 	if 'new_posts' in str(topic['TopicArn']):
# 		topic_arn = topic['TopicArn']
#		print(topic_arn)

# open the payload function which is in the zip file
myutils.zipit ('./convertoaudio.py', './payload2.zip')

with open('./payload2.zip', 'rb') as f:
  zipped_code = f.read()
response = lambda_client.create_function(
  FunctionName=function_name,
  Runtime='python2.7',
  Description= "This function converts the text from s3 to polly mp3",
  Role=role_arn,
  MemorySize= 128,
  Handler='convertoaudio.lambda_handler',
  Code=dict(ZipFile=zipped_code),
  Timeout=300, # Maximum allowable timeout
  Environment={
  		'Variables':{
  			"BUCKET_NAME": bucket_out,
        "DB_TABLE_NAME": table_name
  		}
  },
)
fname = f'Creating Lambda function {function_name}'
myutils.myprint ('INFO', fname, response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))