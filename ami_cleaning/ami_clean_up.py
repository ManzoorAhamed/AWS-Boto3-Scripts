#!/opt/anaconda3/bin/python

## Modules
import boto3
import datetime
from dateutil.parser import parse

client = boto3.client("ec2")
my_ami = client.describe_images(Owners=['self'])['Images']

## Variables
current_date = datetime.datetime.now()
max_ami_age = 120

## Iterating through ami
for ami in my_ami:
    creation_date = ami['CreationDate']
    creation_date_parse = parse(creation_date).replace(tzinfo=None)
    ami_id = ami['ImageId']
    diff_in_days = (current_date - creation_date_parse).days
    if diff_in_days > max_ami_age:
        print("Cleaning up the AMI older than %s days"%max_ami_age)
        client.deregister_image(ImageId=ami_id,DyRun=True)               ## Deregistering the AMI


## Enhance the code to different regions
## Function to data
## For some reason session doesnt work
