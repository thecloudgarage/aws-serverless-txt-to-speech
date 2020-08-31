#!/bin/bash

if [ -z "$LAMBDA_POLICY" ]
then
	echo "Please set LAMBDA_POLICY env var to policy name"
	exit 1
fi
if [ -z "$LAMBDA_ROLE" ]
then
	echo "Please set LAMBDA_ROLE env var to policy name"
	exit 1
fi
echo "Detaching role:$LAMBDA_ROLE and policy:$LAMBDA_POLICY"

policy_arn=`aws iam list-attached-role-policies --role-name $LAMBDA_ROLE|egrep '(PolicyArn)' | awk -F' ' '{print $2}'|sed 's/\"//g'`
policy_name=`aws iam list-attached-role-policies --role-name $LAMBDA_ROLE|egrep '(PolicyName)'|awk -F' ' '{print $2}'|sed 's/\"//g'`
if [ $policy_arn != '' ]
then
	echo "role = $policy_name arn = $policy_arn"
	aws iam detach-role-policy  --role-name $LAMBDA_ROLE --policy-arn $policy_arn
	echo "Deleting Policy $policy_name"
	aws iam delete-policy --policy-arn $policy_arn
else
	echo "Could not detach or delete policy becuase unable to find Policy ARN"
	exit 1
fi

echo "Deleting the Role"
aws iam delete-role --role-name $LAMBDA_ROLE

function_name=PostReader_ConvertToAudio
stmt_id='lambda-policy-for-sns-invoke-1'
echo "Removing permission for sns"
aws lambda remove-permission --function-name $function_name --statement-id $stmt_id

