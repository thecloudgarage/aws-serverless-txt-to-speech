#!/usr/bin/python3
import boto3, json 
import os
import sys
sys.path.append('../../lib')
import myutils
'''
Remove Lambda invocation perms from api gateway

'''

myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
lam = boto3.client('lambda')
# lambda functionst that is granting invoke perm to api gateway
function_names = ['PostReader_NewPosts', 'PostReader_GetPosts',  'PostReader_ConvertToAudio']
for fn in function_names:

	# Give the api deployment permission to trigger the lambda function
	response = lam.remove_permission(
	    FunctionName=fn,
	    StatementId='apigateway-lambda-invoke-perms-' + fn
)
myutils.myprint ('INFO', 'Deleting LAMBDA invoke permissions', response)
print (json.dumps(response, indent=4, sort_keys=True, default=str))