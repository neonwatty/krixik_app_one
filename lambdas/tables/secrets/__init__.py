import os
import boto3
import secrets
from boto3.dynamodb.conditions import Key


aws_profile = os.getenv("AWS_PROFILE")

if aws_profile:
    session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")
else:
    session = boto3.Session(region_name="us-west-2")
dynamodb_resource = session.resource("dynamodb")
table_name = "secrets-ledger"
api_id_gsi_index = "api_id-index"
api_key_gsi_index = "api_key-index"


def generate_api_key(length: int = 64) -> str:
    return secrets.token_urlsafe(length)
