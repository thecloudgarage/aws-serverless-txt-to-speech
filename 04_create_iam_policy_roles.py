#!/usr/bin/python3
import boto3
import json
import os
import sys
sys.path.append('./lib')
import myutils

role_name= os.environ.get('LAMBDA_ROLE', 'sk-lambda-role')
policy_name= os.environ.get('LAMBDA_POLICY', 'sk-lambda-policy')



# Create IAM client
iam = boto3.client('iam')

# Create a policy
my_managed_policy = {
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Action": [
	                "polly:SynthesizeSpeech",
	                "dynamodb:Query",
	                "dynamodb:Scan",
	                "dynamodb:PutItem",
	                "dynamodb:UpdateItem",
	                "sns:Publish",
	                "s3:PutObject",
	                "s3:PutObjectAcl",
	                "s3:GetBucketLocation",
	                "logs:CreateLogGroup",
	                "logs:CreateLogStream",
	                "logs:PutLogEvents"
	            ],
	            "Resource": [
	                "*"
	            ]
	        }
	    ]
	}
response = iam.create_policy(
  PolicyName=policy_name,
  PolicyDocument=json.dumps(my_managed_policy)
)
policy_arn=response['Policy']['Arn']
myutils.myprint ('INFO', 'Creating new IAM Policy for Lambda to access s3,sns,polly,dynamodb,logs', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
AssumeRoledoc= {
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    }
                }
            ],
            "Version": "2012-10-17"
        }
response = iam.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(AssumeRoledoc),
    Description=role_name
)
myutils.myprint ('INFO', 'Creating new Lambda Role', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))
# Attach a role policy
response = iam.attach_role_policy(
    PolicyArn=policy_arn,
    RoleName=role_name
)
myutils.myprint ('INFO', 'Attaching Lambda policy to Lambda Role', response)
#print (json.dumps(response, indent=4, sort_keys=True, default=str))