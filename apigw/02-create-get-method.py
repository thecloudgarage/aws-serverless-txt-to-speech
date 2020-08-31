#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../lib')
import myutils
'''
   Create and setup the GET method for our API
   Only function used is lambda: PostReader_GetPosts

'''
function_name = 'PostReader_GetPosts'
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

query_field='postId'
query_string='method.request.querystring.' + query_field

#Create the GET method in the Resource
response = apigw.put_method(
    restApiId=api_id,
    resourceId=root_id,
    httpMethod='GET',
    authorizationType='NONE',
    requestParameters={
        query_string: False
    }
)
myutils.myprint ('INFO', 'Creating GET Method for REST API', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))

# method integration
# first, get the function arn
res = lam.get_function(FunctionName=function_name)
function_arn=res['Configuration']['FunctionArn']

uri_string = 'arn:aws:apigateway:' + region + ':lambda:path/2015-03-31/functions/' + function_arn + '/invocations'
template="{\r\n    \"postId\" : \"$input.params('postId')\"\r\n}"

#print ("uri = " + uri_string)

response = apigw.put_integration(
	restApiId=api_id,
    resourceId=resource_id,
    cacheNamespace=resource_id,
    httpMethod='GET',
    contentHandling='CONVERT_TO_TEXT',
    type='AWS',
    integrationHttpMethod='POST',
    uri=uri_string,
    passthroughBehavior= 'WHEN_NO_TEMPLATES',
    requestTemplates={
        'application/json': template
    }
	)
myutils.myprint ('INFO', 'Creating integration for GET method ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# Add method Response section
response = apigw.put_method_response(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)
myutils.myprint ('INFO', 'Creating method response for GET method ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))

# put_integration_response(**kwargs)
response = apigw.put_integration_response(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    },
    responseTemplates={
        'application/json': ''
    },
    contentHandling='CONVERT_TO_TEXT'
)
myutils.myprint ('INFO', 'Creating integration method response for GET method ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
