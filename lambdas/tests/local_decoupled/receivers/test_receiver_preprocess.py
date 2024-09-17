import pytest
import os
import json
import time
import boto3
import requests
from botocore.exceptions import ClientError
from sqs.messages.message_poll import message_poll_no_id
from sqs.messages.message_delete import message_delete
from tests.utilities.execute_subprocess import execute_subprocess_command
from tests.utilities.receiver_utilities import step_setup, s3sqs_event_maker
from tests.utilities.docker_utilities import print_container_logs
from config import APP_NAME_PRIVATE, STAGE, ACCOUNT_ID


# get current directory paths
current_directory = os.getcwd()
home_dir = os.path.expanduser("~")

# define docker variables
DOCKER_PORT = 9000
LAMBDA_ENDPOINT = f"http://localhost:{DOCKER_PORT}/2015-03-31/functions/function/invocations"

# Define your test parameters
RECEIVER_NAME = "receiver_preprocess"
BUCKET_TEST = f"{APP_NAME_PRIVATE}-trigger-{STAGE}"
TEST_STATUS_QUEUE = f"{APP_NAME_PRIVATE}-receiver_status-{STAGE}"
TEST_RECEIVERS_QUEUE = f"{APP_NAME_PRIVATE}-{RECEIVER_NAME}-{STAGE}"

# define session
aws_profile = os.getenv("AWS_PROFILE")
session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")

# define clients
s3_client = session.client("s3")
lambda_client = session.client("lambda")

# test file data
test_file_name = "receiver_start"
test_file_path = "tests/test_files/test_file.mp4"

@pytest.fixture(scope="module")
def container_controller():
    # build image
    print("INFO: starting image building process...")
    command = ["bash", "build_image.sh", STAGE, RECEIVER_NAME]
    stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")
    print("INFO: ...complete!")

    # startup container
    command = [
        "docker",
        "run",
        "--env-file",
        "../.env",
        "-e",
        f"STAGE={STAGE}",
        "-e",
        f"RECEIVER_NAME={RECEIVER_NAME}",
        "-d",
        "-v",
        f"{home_dir}/.aws:/root/.aws",
        "--name",
        RECEIVER_NAME,
        "-p",
        f"{DOCKER_PORT}:8080",
        f"{ACCOUNT_ID}-{RECEIVER_NAME}",
    ]
    print("INFO: starting container running process...")
    stdout = execute_subprocess_command(command)
    print("INFO: ...complete!")

    # let container startup before sending post tests
    time.sleep(5)

    yield

    # stop and remove container
    command = ["docker", "stop", RECEIVER_NAME]
    print("INFO: starting container stopping process...")
    stdout = execute_subprocess_command(command)
    print("INFO: ...complete!")

    command = ["docker", "rm", RECEIVER_NAME]
    print("INFO: starting container removal process...")
    stdout = execute_subprocess_command(command)
    print("INFO: ...complete!")


def test_success(container_controller, subtests):
    print("INFO: starting test_success")
    ### setup step ###
    file_id, request_id, s3_key, s3_key_save, receiver_receipt_handle = step_setup(
        subtests, test_file_name, test_file_path, BUCKET_TEST, TEST_RECEIVERS_QUEUE, RECEIVER_NAME, step_progress="in_progress"
    )
    event = s3sqs_event_maker(BUCKET_TEST, s3_key, TEST_RECEIVERS_QUEUE, receiver_receipt_handle)
    print(f"sqs event maker complete")
    # execute lambda in local docker container
    with subtests.test(msg="execute docker lambda locally"):
        # Send a POST request to the Lambda function
        response = requests.post(LAMBDA_ENDPOINT, data=json.dumps(event), headers={"Content-Type": "application/json"})

        # print docker logs
        print_container_logs(RECEIVER_NAME)

        # check response successful, and tables / files look as they should given success
        assert response.status_code == 200
        body = response.json()["body"]
        assert "s3_key_save" in list(body.keys()), "FAILURE: return value s3_key_save from execution not present"
        assert "bucket_name_save" in list(body.keys()), "FAILURE: return value bucket_name_save from execution not present"
        assert "receiver_name" in list(body.keys())
        assert body["receiver_name"] == RECEIVER_NAME
        s3_key_save = body["s3_key_save"]
        bucket_name_save = body["bucket_name_save"]
        content = json.loads(response.content.decode("utf-8"))
        assert content["statusCode"] == 200

    # check for message in test queue
    status_receipt_handle = None
    with subtests.test(msg="check message queue"):
        # poll queue
        queue_data = message_poll_no_id(TEST_STATUS_QUEUE)

        # unpack queue data
        message_id = queue_data["message_id"]
        message = queue_data["message"]
        status_receipt_handle = queue_data["receipt_handle"]

        # unpack message
        assert message["lambda"] == RECEIVER_NAME
        assert message["status"] == "complete"

    # delete receiver message
    with subtests.test(msg="delete receiver message"):
        delete_response = message_delete(TEST_RECEIVERS_QUEUE, receiver_receipt_handle)
        assert delete_response is True

    # delete status message
    with subtests.test(msg="delete status message"):
        delete_response = message_delete(TEST_STATUS_QUEUE, status_receipt_handle)
        assert delete_response is True

    # check output file exists
    with subtests.test(msg="check that output file now exists"):
        s3_client.head_object(Bucket=bucket_name_save, Key=s3_key_save)

    # check that input file is deleted
    with subtests.test(msg="check that test file is deleted"):
        try:
            s3_client.head_object(Bucket=bucket_name_save, Key=s3_key)
        except ClientError as e:
            # If a ClientError is raised, the object does not exist, which is expected
            if e.response["Error"]["Code"] == "404":
                # Object does not exist, so the deletion was successful
                assert True, f"FAILURE: Test object still exists after attempted deletion at {bucket_name}/{s3_key}"
            else:
                # Re-raise the exception if it's not a 404 error
                raise False

    # delete output test file
    with subtests.test(msg="delete test output file"):
        response = s3_client.delete_object(Bucket=BUCKET_TEST, Key=s3_key_save)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 204, f"FAILURE: deletion failed {BUCKET_TEST}/{s3_key}"
