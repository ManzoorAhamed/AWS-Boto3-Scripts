#!/opt/anaconda3/bin/python
## Modules
import boto3
import argparse

## Create Parser
parser = argparse.ArgumentParser()

## Add the arguments
parser.add_argument("--aws_profile",help="AWS profile name")
parser.add_argument("--brand",help="Magazine brand name")
parser.add_argument("--env", help="Environment dev|qa|prod")
parser.add_argument("--function", help="origin|proxy|editor|mysql")

## Execute the parse_arg() method
args = parser.parse_args()

## Filter variables  Based on the args have to construct the filters.
if args.env and args.brand and args.function:
    filters = [{'Name':'tag:legacy.ti_role', 'Values':[str(args.brand)]},{'Name':'tag:legacy.ti_env','Values':[str(args.env)]},{'Name':'legacy.ti_function','Values':[str(args.function)]}]
elif args.env and args.brand:
    filters = [{'Name':'tag:legacy.ti_role', 'Values':[str(args.brand)]},{'Name':'tag:legacy.ti_env','Values':[str(args.env)]}]
elif args.brand and args.function:
    filters = [{'Name':'tag:legacy.ti_role', 'Values':[str(args.brand)]},{'Name':'legacy.ti_function','Values':[str(args.function)]}]
elif args.env and args.function:
    filters = [{'Name':'tag:legacy.ti_env','Values':[str(args.env)]},{'Name':'legacy.ti_function','Values':[str(args.function)]}]
else:
    filters = [{'Name':'tag:legacy.ti_role', 'Values':[str(args.brand)]}]

session = boto3.Session(profile_name=args.aws_profile, region_name='us-east-1')
client = session.client('ec2')
response = client.describe_instances(Filters=filters)

for each_instances in response['Reservations']:
    for each_instance in each_instances['Instances']:
        matchhost = False
        for each_tag in each_instance['Tags']:
            if each_tag['Key'] == 'lifecycle_status_id' and 'live' in each_tag['Value']:
                matchhost = True

        if matchhost:
            response = client.create_tags(Resources=[each_instance['InstanceId']],
                        Tags = [ { 'Key' : 'lifecycle_status_id', 'Value' : 'decomm'}])
            print("Tags updated for the instance %s"%each_instance['InstanceId'])
