#!/usr/bin/python3
import boto3
import os
import json
import sys
sys.path.append('../lib')
import myutils
table_name= os.environ.get('TABLE_NAME', 'PollyProject')
region=os.environ.get('REGION', 'us-east-1')
topic_name=os.environ.get('TOPIC_NAME', 'new_polly_events')
role_name= os.environ.get('LAMBDA_ROLE', 'sk-lambda-role')
policy_name= os.environ.get('LAMBDA_POLICY', 'sk-lambda-policy')

# Delete dynamodb table
session = boto3.session.Session(region_name=region)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(table_name)
response = table.delete()
myutils.myprint ('INFO', 'Deleting dynamodb Table', table_name)

# delete s3 buckets
s3 = boto3.resource('s3')
bk_in= os.environ.get('BUCKET_IN', 'sk-pollybucket-in')
bk_out= os.environ.get('BUCKET_OUT', 'sk-pollybucket-out')
buckets=[]
buckets.append(bk_in)
buckets.append(bk_out)
for bucket in buckets:
	s3_bucket = s3.Bucket(bucket)
	response = s3_bucket.objects.all().delete()
	myutils.myprint ('INFO', 'Deleting bucket objects', response)
	#print (json.dumps(response, indent=4, sort_keys=True, default=str))
	response = s3_bucket.delete()
	myutils.myprint ('INFO', 'Deleting buckets', response)
	#print (json.dumps(response, indent=4, sort_keys=True, default=str))

#delete SNS topic
sns = boto3.client('sns')
topics = sns.list_topics()
for topic in topics["Topics"]:
	if topic_name in str(topic['TopicArn']):
		topic_arn = topic['TopicArn']

response = sns.list_subscriptions_by_topic(
    TopicArn=topic_arn    
    )
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# Get a list of subscriptions from the response
# subscriptions = [subscription for subscription in response['Subscriptions']]
sns = boto3.resource('sns')

subscriptions = []
for subscription in response['Subscriptions']:
    print("removing subscription: %s" % subscription['SubscriptionArn'])
    subs = sns.Subscription(subscription['SubscriptionArn']).delete()

sns = boto3.client('sns')
response = sns.delete_topic(
	TopicArn=topic_arn
	)
myutils.myprint ('INFO', 'Deleting SNS topic', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))

# IAM
# Run the delete_iam.sh script

