#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('../../lib')
import myutils

'''
Delete the top level restApi 

'''

myapi_name=os.environ.get('API_NAME', 'ServerLessPollyAPI')
#myapi_name = 'PostReaderAPI'
apigw = boto3.client('apigateway')
ids = myutils.get_api_ids(myapi_name)
api_id = ids['api_id']
response = apigw.delete_rest_api(restApiId=api_id)
myutils.myprint ('INFO', 'Deleting REST API', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
