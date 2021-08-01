#!/opt/anaconda3/bin/python

## Module
import boto3
from datetime import datetime, timezone

## Create a session if you want to specify the specific profile
clises = boto3.Session(profile_name='profile_name')

## AWS Service
client = clises.client('iam')

## Paginator because iam returns only 100 user per request if more than 100 users use paginator
paginator = client.get_paginator('list_users')

## Variables
current_date = datetime.now(timezone.utc)
max__key_age = 90

## Looping through the users list
for response in paginator.paginate():
    for user in response['Users'] :
        username = user['UserName']                                              ## Retrive the user name
        list_key = client.list_access_keys(UserName=username)                    ## Retrive the access key details
        for access_key in list_key['AccessKeyMetadata']:                         ## Looping through the details
            accesskey_id = access_key['AccessKeyId']                             ## Fetch the key_id
            key_creation_date = access_key['CreateDate']                         ## Fetch the creation date
            age = (current_date - key_creation_date).days                        ## Days difference
            if age > max__key_age:                                               ## Check if its older than max_age
                print('Deactivating the key for the following user '+ username)  ## Print the Message
                ## Deactivate the key if the age is more than 90 days
                client.update_access_key(UserName=username, AccessKeyId=accesskey_id, Status='Inactive')
                                                                                 ##  Deactivate the key


