#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('./lib')
import myutils

'''
 Add the API endpoint in the javascript
 upload all static files to the static website on s3

'''
bk_in = os.environ.get('BUCKET_IN', 'sk-pollybucket-in')
myapi_name = os.environ.get('API_NAME', 'ServerLessPollyAPI')
stage_name = os.environ.get('STAGE_NAME', 'development')
region = os.environ.get('REGION', 'us-east-1')
folder='./site_files/'
template = folder + '_scripts.js'
outfile = folder + 'scripts.js'
s3 = boto3.client("s3")

bucket_name = bk_in
object_list = ['scripts.js', 'styles.css', 'index.html']

# Add the API end point to the _scripts.js file to generate scripts.js
# var API_ENDPOINT = "https://{api-id}.execute-api.{us-east-1}.amazonaws.com/{stagename}"
url = myutils.get_api_invoke_url(myapi_name, stage_name)
api_id = myutils.get_api_ids(myapi_name)['api_id']
add_str = f'var API_ENDPOINT = "https://{api_id}.execute-api.{region}.amazonaws.com/{stage_name}"'
print ("Generating scripts.js file with API ENDPOINT " + '\n' + add_str)

try:
    with open(template, 'r+') as f:
        template_content = f.read()
    try:
        with open(outfile, 'w') as out:
            out.seek(0, 0)
            out.write(add_str + '\n' + template_content)
    except (IOError):
        print ("Could not write to file" + outfile)

except (IOError):
    print("Could not open template file" + template)

for item in object_list:
    try:
        fname=folder + item
        body=open(fname, 'rb')
        response = s3.put_object(Bucket=bucket_name, Key=item,
            Body=body, ContentType='text/html')
        fname = f'Adding {item} to S3 bucket {bucket_name}'
        response = dict(response)
        myutils.myprint('INFO', fname, response)
        print ('File:' + str(item) + ' upload status = HTTP ' + str(response['ResponseMetadata']['HTTPStatusCode']))
    except Exception as error:
        print (error)
