#!/usr/bin/python3
import boto3
import json
import sys
import os
sys.path.append('../../lib')
import myutils


myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')

ids = myutils.get_api_ids(myapi_name)
myapi_id=ids['api_id']
root_id=ids['root_id']
resource_id = ids['resource_id']

apigw = boto3.client('apigateway')

print ("--------------------API---------------------------------------")
response = apigw.get_rest_api(
     restApiId=myapi_id 
)
print (json.dumps(response, indent=4, sort_keys=True, default=str))
print ("-------------------------GET----------------------------------")

response = apigw.get_method(
	restApiId=myapi_id,
	resourceId=resource_id,
	httpMethod='GET'
	)
print (json.dumps(response, indent=4, sort_keys=True, default=str))
print ("-----------------------POST------------------------------------")
response = apigw.get_method(
	restApiId=myapi_id,
	resourceId=resource_id,
	httpMethod='POST'
	)
print (json.dumps(response, indent=4, sort_keys=True, default=str))
print ("-----------------------OPTIONS/MOCK---------------------------------")
response = apigw.get_integration(
	restApiId=myapi_id,
	resourceId=resource_id,
	httpMethod='OPTIONS'
	)
print (json.dumps(response, indent=4, sort_keys=True, default=str))

response = apigw.get_resources (
	restApiId=myapi_id
	)
print ("-----------------------GET_resources_OUTput---------------------------------")
print (json.dumps(response, indent=4, sort_keys=True, default=str))

response= apigw.get_resource(
	restApiId=myapi_id,
	resourceId=resource_id
	)
print ("-----------------------GET_resource_OUTput---------------------------------")
print (json.dumps(response, indent=4, sort_keys=True, default=str))