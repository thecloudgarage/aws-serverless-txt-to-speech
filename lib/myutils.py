#!/usr/bin/python3
import json
import boto3
import os
import sys
from datetime import datetime
from zipfile import ZipFile 

'''
Given an REST API Name, it will return the api ID, the root ID and the resource ID
'''

PROJECT_DIR=os.environ.get('PROJECT_DIR', '')
LOG_DIR=os.environ.get('LOG_DIR', 'logs')
LOG_FILE_NAME=os.environ.get('LOG_FILE', 'app-deployment.log')

LOG_FILE=PROJECT_DIR + '/' + LOG_DIR + '/' + LOG_FILE_NAME
def get_api_ids(apiName):
	apigw = boto3.client('apigateway')
	api_id=''
	root_id=''
	resource_id = ''

	response = apigw.get_rest_apis()
	for item in response['items']:
		if item['name'] == apiName:
			api_id = item['id']
			#print ("match found id= " + api_id)
	resources = apigw.get_resources(restApiId=api_id)
	root_id = [resource for resource in resources['items'] if resource['path'] == '/'][0]['id']
	resource_id = root_id
	#print ("root_id = " + resource_id)
	
	ret_dict = {
		'api_id' : api_id,
		'resource_id': resource_id,
		'root_id': root_id
	}
	return ret_dict

def get_account_id():
	return boto3.client('sts').get_caller_identity().get('Account')

def myprint(category, outputFrom, inputstring):
	# category = INFO or ERROR, str
	# inputstring is a dict
	# outputFrom is str
	input = json.dumps(inputstring, indent=4, sort_keys=True, default=str)
	sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
	#print ('logfile = ', LOG_FILE)
	try:
	    with open(LOG_FILE, 'a') as logfile:
	        logfile.write(category + ':' + sttime  
	        	+ ':' + outputFrom + ': =======================================\n' 
	        	+ input + '\n =================== END OF OUTPUT ====================\n')
	    return 0
	except IOError:
	   	print ("Failed to write to log file")
	return -1
	 

def get_api_invoke_url(apiName,stageName):
	region=os.environ.get('REGION', 'us-east-1')
	api_id = get_api_ids(apiName)['api_id']
	url=f'https://{api_id}.execute-api.{region}.amazonaws.com/{stageName}'
	return url

def zipit (sourceFile, targetZip):

	# writing files to a zipfile 
    with ZipFile(targetZip,'w') as zip: 
        # writing each file one by one 
        zip.write(sourceFile) 
    print('File zipped successfully!') 

