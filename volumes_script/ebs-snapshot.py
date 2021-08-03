#!/opt/anaconda3/bin/python

## Modules
import boto3

ec2 = boto3.resource("ec2")
volumes = ec2.volumes.all()

for vol in volumes:
    vol_id = vol.id
    volumes = ec2.Volume(vol_id)
    desc = "This is the snapshot of the volume {}".format(vol_id)
    print("Creating the snapshot of the following volume "+vol_id)
    volumes.create_snapshot(Description=desc)
