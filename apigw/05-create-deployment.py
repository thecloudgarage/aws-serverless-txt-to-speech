#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../lib')
import myutils
myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
stage_name=os.environ.get('API_STAGE_NAME','development')

#---------------------------DO NOT CHANGE ANYTHING BELOW -------------

apigw = boto3.client('apigateway')

ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']

#print ('api id = ' + api_id + ' root id = ' + root_id + ' resource id = ' + resource_id)
# Deploy our API
response = apigw.create_deployment(
    restApiId=api_id,
    stageName=stage_name,
    stageDescription='Polly development gateway',
    description='Polly development gateway'
    
)
myutils.myprint ('INFO', 'Creating new Deployment', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))

# Update the throttling to ensure, we dont get charged too much for
# bots and script kiddies.
response = apigw.update_stage(
    restApiId=api_id,
    stageName=stage_name,
    patchOperations=[
             {
                'op': 'replace',
                'path': '/*/*/throttling/burstLimit',
                'value': '5',
            },
            {
                'op': 'replace',
                'path': '/*/*/throttling/rateLimit',
                'value': '2',
            }
        ]

	)
myutils.myprint ('INFO', 'Updating Deployment STAGE for throttles', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))