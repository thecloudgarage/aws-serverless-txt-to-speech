#!/usr/bin/python3
import boto3
import os
import json
import sys
sys.path.append('./lib')
import myutils
table_name= os.environ.get('TABLE_NAME', 'PollyProject')
region=os.environ.get('REGION', 'us-east-1')

session = boto3.session.Session(region_name=region)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(table_name)
new_table = dynamodb.create_table(
    KeySchema=[
        {
            'AttributeName' : 'id',
            'KeyType' : 'HASH',
        },
    ],
    TableName=table_name,
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
    AttributeDefinitions= [
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }
        ]
)
# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
myutils.myprint ('INFO', 'Creating new dynamodb Table', new_table)
