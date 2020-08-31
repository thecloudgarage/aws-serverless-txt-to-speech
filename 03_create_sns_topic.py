#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('./lib')
import myutils
'''
 step 3
 create a SNS topic to publish to
'''
topic_name=os.environ.get('TOPIC_NAME', 'new_polly_events')

sns = boto3.client('sns')
response = sns.create_topic(
    Name=topic_name,
    Attributes={
        'DisplayName': 'New Posts'
    }
)
myutils.myprint ('INFO', 'Creating new SNS topic', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
