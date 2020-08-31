#!/usr/bin/python3
'''
  create 2 buckets. BUCKET_IN is our STATIC website. Bucket_out is the s3 repo for mp3s
  uses your source IP address in bucket policy condition
  Checks for command line args first and then BUCKET_IN and BUCKET_OUT env vars
  If it cant find in either method, throws error

'''
import boto3
import json
import os
from requests import get
import sys
sys.path.append('./lib')
import myutils

my_external_ip=get('https://ipapi.co/ip/').text
ip_string='0.0.0.0/0'

bk_in= os.environ.get('BUCKET_IN', 'sk-pollybucket-in')
bk_out= os.environ.get('BUCKET_OUT', 'sk-pollybucket-out')
def usage():
	print ("USAGE: scriptname 'in-bucket-name' 'out-bucket-name'")
	print ("or set environment vars BUCKET_IN, BUCKET_OUT and run with no params")

def create_buckets(bk_in, bk_out):
	s3 = boto3.resource('s3')
	buckets=[]
	buckets.append(bk_in)
	buckets.append(bk_out)
	for bucket in buckets:
		response =s3.create_bucket(Bucket=bucket)
		myutils.myprint ('INFO', 'Creating new S3 buckets', response)
		#print (json.dumps(response, indent=4, sort_keys=True, default=str))
	# Turn bucket_in to a website
	website_payload = {
		    'ErrorDocument': {
		        'Key': 'error.html'
		    },
		    'IndexDocument': {
		        'Suffix': 'index.html'
		    }
	}
	bucket_website = s3.BucketWebsite(bk_in)
	# And configure the static website with our desired index.html
	# and error.html configuration.
	bucket_website.put(WebsiteConfiguration=website_payload)

	# Create an S3 client
	s3 = boto3.client('s3')
	for bucket in buckets:
		# Create the bucket policy
		bucket_policy = {
		    'Version': '2012-10-17',
		    'Statement': [{
		        'Sid': 'AddPerm',
		        'Effect': 'Allow',
		        'Principal': '*',
		        'Action': ['s3:GetObject'],
		        "Condition": {
		         "IpAddress": {"aws:SourceIp": ip_string}
		         },
		        'Resource': "arn:aws:s3:::%s/*" % bucket
		    }]
		}

		# Convert the policy to a JSON string
		bucket_policy = json.dumps(bucket_policy)
		# Set the new policy on the given bucket
		response = s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
		myutils.myprint ('INFO', 'Updating bucket policies', response)
		#print (json.dumps(response, indent=4, sort_keys=True, default=str))

if len(sys.argv) != 3:
	if bk_in and bk_out:
		 create_buckets(bk_in, bk_out)
		
elif len(sys.argv) == 3:
		buckets=sys.argv[1:]
		create_buckets(sys.argv[1], sys.argv[2])
else:
		print ("Error: Could not get required bucket parameters ")
		usage()

