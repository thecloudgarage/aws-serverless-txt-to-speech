#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../lib')
import myutils
'''
   POST function setup in API Gateway.
   calls Lambda: PostReader_NewPosts

'''

lambda_function='PostReader_NewPosts'
myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
region=os.environ.get('REGION', 'us-east-1')
#---------------------------DO NOT CHANGE ANYTHING BELOW -------------
apigw = boto3.client('apigateway')
lam = boto3.client('lambda')

ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']


# GET Method query string
# needed to search as http://xxx/?postId=2837481748
query_field='postId'
query_string='method.request.querystring.' + query_field

# Create the GET method in the Resource
response = apigw.put_method(
    restApiId=api_id,
    resourceId=root_id,
    httpMethod='POST',
    authorizationType='NONE',
    requestParameters={}
    
)
myutils.myprint ('INFO', 'Creating POST method for API ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))

# method_response
response = apigw.put_method_response(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)
myutils.myprint ('INFO', 'Creating method response for POST method ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))

# method_integration
res = lam.get_function(FunctionName=lambda_function)
function_arn=res['Configuration']['FunctionArn']


uri_string = 'arn:aws:apigateway:' + region + ':lambda:path/2015-03-31/functions/' + function_arn + '/invocations'
response = apigw.put_integration(
	restApiId=api_id,
    resourceId=resource_id,
    cacheNamespace=resource_id,
    httpMethod='POST',
    contentHandling='CONVERT_TO_TEXT',
    type='AWS',
    integrationHttpMethod='POST',
    uri=uri_string,
    passthroughBehavior= 'WHEN_NO_MATCH'
	)
myutils.myprint ('INFO', 'Creating method integration for POST method ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# integration_response
response = apigw.put_integration_response(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    },
    responseTemplates={
        'application/json': ''
    }
)
myutils.myprint ('INFO', 'Creating method integration response for POST method ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))