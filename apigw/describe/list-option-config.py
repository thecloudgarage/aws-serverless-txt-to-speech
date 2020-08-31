#!/usr/bin/python3
import boto3, json
import sys
import os
sys.path.append('../../lib')
import myutils


myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')

ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']

apigw = boto3.client('apigateway')
lam = boto3.client('lambda')

response = apigw.get_integration(
	restApiId=api_id,
	resourceId=resource_id,
	httpMethod='OPTIONS'
	)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
myutils.myprint ('INFO', 'get_integration output for OPTIONS', response)