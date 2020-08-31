#!/bin/bash
source ./00_env_vars.sh
echo "Destroying the stack.."
rm -f ./payload.zip
rm -f ./payload2.zip
rm -f ./payload3.zip
rm -f ./site_files/scripts.js
cd ./apigw/undo
echo "Removing API permissions"
./01-delete-lambda-invocation-perms-apigw.py
echo "Removing API deployment.."
./02-delete-deployment.py
echo "Removing REST API"
./03-delete-rest-api.py
cd ../../undo
python3 ./delete_stack.py
echo "Removing IAM permissions.."
./delete_iam.sh
echo "Removing Lambda functions.."
./delete_lambda.sh
echo "All Done. Please login to AWS console to verify"
