#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../lib')
import myutils
'''
Create the top level restApi 

'''
myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')

#myapi_name = 'PostReaderAPI'
apigw = boto3.client('apigateway')

# create the top level API name and ID
response = apigw.create_rest_api(
		name=myapi_name,
		description="My Lambda Polly API",
		endpointConfiguration= {
        	'types': ['REGIONAL']
        }

	)
myutils.myprint ('INFO', 'Creating new REST API ', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
