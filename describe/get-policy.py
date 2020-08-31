#!/usr/bin/python3
import boto3
import json

lam = boto3.client('lambda')
response = lam.get_policy(FunctionName='PostReader_ConvertToAudio')

print (json.dumps(response['Policy'], indent=4))
