#!/usr/bin/python3
import boto3, json 
import os
import sys
sys.path.append('../lib')
import myutils

'''
Final Step. 
This adds the permission in Lambda for apigateway to invoke lambda functions
At this point you can use the TEST button in the Method section of API Console 
to test out. Just enter postId=* in the GET  query string and you should see status 200

'''
myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
region=os.environ.get('REGION', 'us-east-1')

#---------------------------DO NOT CHANGE ANYTHING BELOW -------------


lam = boto3.client('lambda')

ids = myutils.get_api_ids(myapi_name)
api_id=ids['api_id']

account_id=myutils.get_account_id()
# lambda functionst that is granting invoke perm to api gateway
function_names = ['PostReader_GetPosts', 'PostReader_NewPosts', 'PostReader_ConvertToAudio']

uri ='arn:aws:execute-api:' + region + ':' + account_id + ':'  + api_id + '/*'
for fn in function_names:

	# Give the api deployment permission to trigger the lambda function
	response = lam.add_permission(
	    FunctionName=fn,
	    StatementId='apigateway-lambda-invoke-perms-' + fn,
	    Action='lambda:InvokeFunction',
	    Principal='apigateway.amazonaws.com',
	    SourceArn=uri
)
myutils.myprint ('INFO', 'Adding Lambda invoke permission for API Gateway', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))