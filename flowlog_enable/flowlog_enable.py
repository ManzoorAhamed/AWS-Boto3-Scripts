#!/opt/anaconda3/bin/python

## Modules
import boto3
from botocore.exceptions import ClientError

client = boto3.client("ec2")                                                   ## client object for ec2
client_logs = boto3.client('logs')                                             ## client object for cloud watch log
response = client.describe_vpcs()                                              ## Collecting all VPC details
for vpc in response['Vpcs']:                                                   ## Loop through the reponse to fetch the vpc id
    vpc_id = vpc['VpcId']                                                      ## Assign the values to the variable

    log_group = vpc_id + "-flowlog"                                            ## Loggroup Name

    try:                                                                       ## try except block to check the existence of log group
        response = client_logs.create_log_group(logGroupName=log_group)        ## trying to create the loggroup
        print("Created the log group",log_group)                               ## if it's success it will print the message
    except ClientError:                                                        ## In case loggroup already exists will throw client error
        print("The log exists for the vpc_id",vpc_id)                          ## Print saying log group already exists

    flow_log_filter = {'Name':'resource-id','Values':[vpc_id]}                 ## Framing the filter
    response_flow_logs = client.describe_flow_logs(Filters=[flow_log_filter])  ## Describe the flow log
    if len(response_flow_logs['FlowLogs']) > 0:                                ## check the length of the response_flow_logs['FlowLogs'] > 0
        print("Vpc flowLog enabled for the vpc",vpc_id)                        ## if enabled print the msg
    else:
        print("Enabling the flowlog for the following vpc_id",vpc_id)          ## Prints the msg and enable the flow log.
        response = client.create_flow_logs(
            ResourceIds=[vpc_id],
            ResourceType='VPC',
            TrafficType='ALL',
            LogGroupName=log_group,
            DeliverLogsPermissionArn='string',                    ## We need IAM permission to be setup for the vpc log's to be pushed to the cloudwatch.
        )
