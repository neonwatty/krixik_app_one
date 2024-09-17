import pytest
import os
import json
import boto3
from sqs.messages.message_poll import message_poll_no_id
from sqs.messages.message_delete import message_delete
from tests.utilities.execute_subprocess import execute_subprocess_command
from tests.utilities.receiver_utilities import step_setup, s3sqs_event_maker
from config import APP_NAME_PRIVATE, STAGE

# get current directory paths
current_directory = os.getcwd()
home_dir = os.path.expanduser("~")

# Define your test parameters
RECEIVER_NAME = "receiver_end"
BUCKET_TEST = f"{APP_NAME_PRIVATE}-trigger-{STAGE}"
TEST_STATUS_QUEUE = f"{APP_NAME_PRIVATE}-receiver_status-{STAGE}"
TEST_RECEIVERS_QUEUE = f"{APP_NAME_PRIVATE}-{RECEIVER_NAME}-{STAGE}"
SERVERLESS_NAME = "serverless_receivers.yml"
LAMBDA_FUNCTION_NAME = f"{APP_NAME_PRIVATE}-{RECEIVER_NAME}-{STAGE}"

# define session
aws_profile = os.getenv("AWS_PROFILE")
session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")

# define clients
s3_client = session.client("s3")
lambda_client = session.client("lambda")

# test file data
test_file_name = "receiver_process"
test_file_path = "tests/test_files/test_file.mp4"


@pytest.fixture(scope="module")
def build_deploy():
    # no build / deploy on github yet
    if os.getenv('GITHUB_ACTIONS') is False:
        # build image
        print("INFO: starting image building process...")
        command = ["bash", "build_image.sh", STAGE, RECEIVER_NAME]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")
        print("INFO: ...complete!")

        # deploy image
        print("INFO: starting image deploy process...")
        command = ["bash", "deploy_image.sh", STAGE, RECEIVER_NAME]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")
        print("INFO: ...complete!")

        # deploy lambdas
        print("INFO: starting service deploy process...")
        command = ["bash", "adjust_functions.sh", "deploy", STAGE, SERVERLESS_NAME]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas")
        print("INFO: ...complete!")


def test_success(build_deploy, subtests):
    print("INFO: starting test_success")
    ### setup step ###
    file_id, request_id, s3_key, s3_key_save, receiver_receipt_handle = step_setup(
        subtests, test_file_name, test_file_path, BUCKET_TEST, TEST_RECEIVERS_QUEUE, RECEIVER_NAME, step_progress="in_progress"
    )
    event = s3sqs_event_maker(BUCKET_TEST, s3_key, TEST_RECEIVERS_QUEUE, receiver_receipt_handle)
    print(f"sqs event maker complete")

    # execute function
    with subtests.test(msg="execute function"):
        # invoke lambda
        response = lambda_client.invoke(FunctionName=LAMBDA_FUNCTION_NAME, InvocationType="RequestResponse", Payload=json.dumps(event))

        # check response successful, and tables / files look as they should given success
        assert response["StatusCode"] == 200
        streaming_body = response["Payload"]
        content = json.loads(streaming_body.read().decode("utf-8"))
        assert content["statusCode"] == 200

    # check for message in test queue
    receipt_handle = None
    with subtests.test(msg="check message queue"):
        # poll queue
        queue_data = message_poll_no_id(TEST_STATUS_QUEUE)

        # unpack queue data
        message_id = queue_data["message_id"]
        message = queue_data["message"]
        receipt_handle = queue_data["receipt_handle"]

        # unpack message
        assert message["lambda"] == RECEIVER_NAME
        assert message["status"] == "complete"

    # delete message
    with subtests.test(msg="delete message"):
        delete_response = message_delete(TEST_STATUS_QUEUE, receipt_handle)
        assert delete_response is True

    # delete input test file
    with subtests.test(msg="delete test file"):
        response = s3_client.delete_object(Bucket=BUCKET_TEST, Key=s3_key)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 204, f"FAILURE: deletion failed {BUCKET_TEST}/{s3_key}"
