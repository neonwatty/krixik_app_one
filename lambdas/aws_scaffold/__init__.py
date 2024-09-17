import os
import boto3
from dotenv import load_dotenv

# use env file from base directory - above lambdas
dotenv_path = os.path.join(os.path.dirname(__file__), "../../", ".env")
load_dotenv(dotenv_path)

# get values
AWS_PROFILE = os.getenv("AWS_PROFILE")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
APP_NAME_PRIVATE = os.getenv("APP_NAME_PRIVATE")

if AWS_PROFILE:
    session = boto3.Session(profile_name=AWS_PROFILE, region_name="us-west-2")
else:
    session = boto3.Session(region_name="us-west-2")

# define receiver names
receiver_names = ["receiver_start", "receiver_status", "receiver_preprocess", "receiver_process", "receiver_end"]
