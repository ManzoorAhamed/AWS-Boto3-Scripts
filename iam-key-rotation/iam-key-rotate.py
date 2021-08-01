#!/opt/anaconda3/bin/python

## Module
import boto3
from datetime import datetime, timezone

clises = boto3.Session(profile_name='ioe-sandbox')
client = clises.client('iam')
paginator = client.get_paginator('list_users')

current_date = datetime.now(timezone.utc)
max_age = 90

for response in paginator.paginate():
    for user in response['Users'] :
        username = user['UserName']

        list_key = client.list_access_keys(UserName=username)
        for access_key in list_key['AccessKeyMetadata']:
            access_key_id = access_key['AccessKeyId']
            key_creation_date = access_key['CreateDate']
            age = (current_date - key_creation_date).days
            if age > max_age:
                print('Deactivate the key')


