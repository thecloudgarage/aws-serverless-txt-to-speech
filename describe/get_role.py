#!/usr/bin/python3
import boto3
import json

client = boto3.client('iam')
response = client.get_role(
    RoleName='sk-lambda-role'
)
print (json.dumps(response, indent=4, sort_keys=True, default=str))
