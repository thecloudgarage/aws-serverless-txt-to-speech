#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../../lib')
import myutils

myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
stage_name=os.environ.get('STAGE_NAME','development')

apigw = boto3.client('apigateway')

ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']

print ('api id = ' + api_id + ' root id = ' + root_id + ' resource id = ' + resource_id)
# delete the stage first
response = apigw.delete_stage(
	restApiId = api_id,
	stageName=stage_name
	)
myutils.myprint ('INFO', 'Deleting stage', response)
# now delete the deployments

deployments = apigw.get_deployments(
	restApiId= api_id
	)
for item in deployments['items']:
	if stage_name in item['description']:
		logmsg="Will delete this deployment id = " + item['id'] + " description = " + item['description']
		print(logmsg)

		response = apigw.delete_deployment(
			restApiId=api_id,
			deploymentId=item['id']	
			)
		myutils.myprint ('INFO', 'Deleting deployments', response)
		print (json.dumps(response, indent=4, sort_keys=True, default=str))


