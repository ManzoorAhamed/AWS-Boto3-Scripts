#!/opt/anaconda3/bin/python

## Module
import boto3
import argparse

## Create the argparser
parser = argparse.ArgumentParser()

## Add the arguments
parser.add_argument("profile_name",help="Profile Name of the account")
parser.add_argument("region",help="Region Name")

## Execute the parse_arg() method
args = parser.parse_args()

## Session Creation
session = boto3.Session(profile_name=args.profile_name,region_name=args.region)
ec2 = session.resource('ec2')

## Collecting the region details
regions = []
for region in ec2.meta.client.describe_regions()['Regions']:
    regions.append(region['RegionName'])


for region in regions:
    ec2 = session.resource("ec2",region_name=region)
    ec2_filter = {"Name": "instance-state-name","Values": ["running"]}
    instances = ec2.instances.filter(Filters=[ec2_filter])
    for instance in instances:
        instance.stop()

