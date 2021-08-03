#!/opt/anaconda3/bin/python

## Modules
import boto3
import datetime
from dateutil.parser import parse


client = boto3.client("ec2")
regions = client.describe_regions()
## Variables
current_date = datetime.datetime.now()
max_ami_age = 120
regions_list=[]

## Collecting the region details
for region in regions['Regions']:
    regions_list.append(region['RegionName'])

## Iterating through the available region
for region in regions_list:
    client1 = boto3.client("ec2",region_name=region)
    my_ami = client1.describe_images(Owners=['self'])['Images']
## Iterating through ami
    for ami in my_ami:
        creation_date = ami['CreationDate']
        creation_date_parse = parse(creation_date).replace(tzinfo=None)
        ami_id = ami['ImageId']
        diff_in_days = (current_date - creation_date_parse).days
        if diff_in_days > max_ami_age:
            print("Cleaning up the AMI-ID %s is older than %s days in the %s region"%(ami_id,max_ami_age,region))
            client.deregister_image(ImageId=ami_id,DyRun=True)               ## Deregistering the AMI


## Enhance the code to different regions.            Done
## Function to data.                                Yet to complete
## For some reason session doesnt work.
## Uses default(profile) AWS credentials.
## Script looks for the AMI which is older than 120 days and deregister it. DryRun is set to True.
