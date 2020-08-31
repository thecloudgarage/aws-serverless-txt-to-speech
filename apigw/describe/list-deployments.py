#!/usr/bin/python3
import boto3, json
import sys
import os
sys.path.append('../../lib')
import myutils


myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
stage_name=os.environ.get('STAGE_NAME', 'development')
ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']

apigw = boto3.client('apigateway')
lam = boto3.client('lambda')

response = apigw.get_deployments(
	restApiId=api_id
	)
print (json.dumps(response, indent=4, sort_keys=True, default=str))
#myutils.myprint ('INFO', 'get_integration output for OPTIONS', response)
for item in response['items']:
	print ('deployment ID = ' + item['id'] + ' description =  ' + item['description'])
	stage_res = apigw.get_stage(
		restApiId=api_id,
		stageName=stage_name)
	print (json.dumps(stage_res, indent=4, sort_keys=True, default=str))

api_url = myutils.get_api_invoke_url(myapi_name, stage_name)
print ('API URL = ' + api_url)