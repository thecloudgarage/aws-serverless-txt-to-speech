#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../lib')
import myutils

myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')

#---------------------------DO NOT CHANGE ANYTHING BELOW -------------

apigw = boto3.client('apigateway')
lam = boto3.client('lambda')

ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']


# Create an OPTIONS method
response = apigw.put_method(
	restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'

)
myutils.myprint ('INFO', 'Creating OPTIONS Method for CORS ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# # add method response
response = apigw.put_method_response(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)
myutils.myprint ('INFO', 'Creating OPTIONS Method response for CORS ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# # add Options integration method
response = apigw.put_integration(
	restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    passthroughBehavior= 'WHEN_NO_MATCH',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)
myutils.myprint ('INFO', 'Creating OPTIONS integration for OPTIONS method', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# SETUP CORS 
response = apigw.put_integration_response(
	restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
        responseTemplates={
        'application/json': '{"statusCode": 200}'
    },
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST,GET,OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }

)
myutils.myprint ('INFO', 'Creating OPTIONS integration response and CORS Headers', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
