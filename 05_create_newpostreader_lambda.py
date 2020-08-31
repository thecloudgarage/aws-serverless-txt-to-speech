#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('./lib')
import myutils

'''
  invoked by the POST method of the API
  adds a new request of text to polly item
'''
function_name = 'PostReader_NewPosts'

iam_role= os.environ.get('LAMBDA_ROLE', 'sk-lambda-role')
topic_name=os.environ.get('TOPIC_NAME', 'new_polly_events')
table_name=os.environ.get('TABLE_NAME','PollyProject')

iam = boto3.client('iam')
sns = boto3.client('sns')
lambda_client = boto3.client('lambda')

role_name = iam.get_role(RoleName=iam_role)
role_arn = role_name['Role']['Arn']
topics = sns.list_topics()
for topic in topics["Topics"]:
	if topic_name in str(topic['TopicArn']):
		topic_arn = topic['TopicArn']
#		print(topic_arn)
# Create zip file
myutils.zipit ('./createpost.py', './payload.zip')

# open the payload function which is in the zip file
with open('./payload.zip', 'rb') as f:
  zipped_code = f.read()
response = lambda_client.create_function(
  FunctionName=function_name,
  Runtime='python2.7',
  Description= "this function inserts data info dynamodb table called posts",
  Role=role_arn,
  MemorySize= 128,
  Handler='createpost.lambda_handler',
  Code=dict(ZipFile=zipped_code),
  Timeout=300, # Maximum allowable timeout
  Environment={
  		'Variables':{
  			"DB_TABLE_NAME": table_name,
  			"SNS_TOPIC": topic_arn
  		}
  },
)
fname = f'Creating Lambda function {function_name}'
myutils.myprint ('INFO', fname, response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))