import os
import boto3


aws_profile = os.getenv("AWS_PROFILE")

if aws_profile:
    session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")
else:
    session = boto3.Session(region_name="us-west-2")
sqs_client = session.client("sqs")
