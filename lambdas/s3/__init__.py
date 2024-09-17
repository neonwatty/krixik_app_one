import os
import boto3
from dotenv import load_dotenv

current_directory = os.getcwd()
print(f"INFO: s3 current_directory: {current_directory}")
dotenv_path = os.path.abspath(os.path.join(current_directory, "..", ".env"))
print(f"INFO: s3 dotenv path: {dotenv_path}")
load_dotenv(dotenv_path)

aws_profile = os.getenv("AWS_PROFILE")

if aws_profile:
    session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")
else:
    session = boto3.Session(region_name="us-west-2")
s3_client = session.client("s3")
