import pytest
import os
import json
import boto3
import time
from sqs.messages.message_poll import message_poll_no_id
from sqs.messages.message_delete import message_delete
from tests.utilities.execute_subprocess import execute_subprocess_command
from tests.utilities.receiver_utilities import step_setup, s3sqs_event_maker

# get current directory paths
current_directory = os.getcwd()
home_dir = os.path.expanduser("~")

# define session
aws_profile = os.getenv("AWS_PROFILE")
session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")

# define clients
s3_client = session.client("s3")
lambda_client = session.client("lambda")

# test file data
test_file_name = "receiver_start"
test_file_path = "tests/test_files/blank.jpg"

# variables
APP_NAME_PRIVATE = os.environ["APP_NAME_PRIVATE"]
STAGE = "development"
BUCKET_STAGE = f"{APP_NAME_PRIVATE}-{STAGE}"
RECEIVER_NAME = "receiver_start"
TEST_STATUS_QUEUE = f"{APP_NAME_PRIVATE}-test-status"
TEST_RECEIVERS_QUEUE = f"{APP_NAME_PRIVATE}-test-receivers"
SERVERLESS_NAME = "serverless_receivers.yml"
LAMBDA_FUNCTION_NAME = f"{APP_NAME_PRIVATE}-{RECEIVER_NAME}-{STAGE}"

# list of receivers
receiver_names = ["receiver_start", "receiver_preprocess", "receiver_process", "receiver_preprocess"]


# setup fixture
@pytest.fixture(scope="module")
def receivers_setup():
    # build and deploy function images
    for receiver_name in receiver_names:
        command = ["bash", "build_image.sh", STAGE, receiver_name]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")

        command = ["bash", "deploy_image.sh", STAGE, receiver_name]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")

    time.sleep(5)

    # deploy yamls
    command = ["bash", "adjust_functions.sh", "deploy", STAGE, "serverless_receivers.yml"]
    stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas")


def test_success(receivers_setup, subtests):
    # construct event payload for app
    upload_id = 0
    user_id = 0
    s3_key = "0" * 10
    payload = {
        "message": "File uploaded successfully",
        "upload_id": upload_id,
        "user_id": user_id,
        "file_key": s3_key,
        "bucket_name": BUCKET_STAGE,
        "stage": STAGE,
    }

    # upload test file - first create s3_key
    s3_key_save = f"{user_id}/{upload_id}/receiver_start"

    # upload file
    with subtests.test(msg="create a test file"):
        with open(test_file_path, "rb") as file_data:
            s3_client.put_object(Bucket=BUCKET_STAGE, Key=s3_key, Body=file_data)

    # execute function
    with subtests.test(msg="execute function"):
        # Send a POST request to the Lambda function
        response = lambda_client.invoke(FunctionName=LAMBDA_FUNCTION_NAME, InvocationType="RequestResponse", Payload=json.dumps(payload))

        # check response successful, and tables / files look as they should given success
        assert response["StatusCode"] == 200
        streaming_body = response["Payload"]
        content = json.loads(streaming_body.read().decode("utf-8"))
        assert content["statusCode"] == 200
        body = content["body"]
        assert "s3_key_save" in list(body.keys()), "FAILURE: return value s3_key_save from execution not present"
        assert "bucket_name_save" in list(body.keys()), "FAILURE: return value bucket_name_save from execution not present"
        s3_key_save = body["s3_key_save"]
        bucket_name_save = body["bucket_name_save"]
