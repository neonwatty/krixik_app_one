import pytest
import os
import json
import time
import boto3
import requests
from sqs.messages.message_delete import message_delete
from tests.utilities.execute_subprocess import execute_subprocess_command
from tests.utilities.receiver_utilities import status_setup
from tests.utilities.docker_utilities import print_container_logs
from config import APP_NAME_PRIVATE, STAGE, ACCOUNT_ID

# get current directory paths
current_directory = os.getcwd()
home_dir = os.path.expanduser("~")

# define docker variables
DOCKER_PORT = 9000
LAMBDA_ENDPOINT = f"http://localhost:{DOCKER_PORT}/2015-03-31/functions/function/invocations"

# Define your test parameters
RECEIVER_NAME = "receiver_status"
BUCKET_TEST = f"{APP_NAME_PRIVATE}-trigger-{STAGE}"
TEST_STATUS_QUEUE = f"{APP_NAME_PRIVATE}-receiver_status-{STAGE}"
TEST_RECEIVERS_QUEUE = f"{APP_NAME_PRIVATE}-{RECEIVER_NAME}-{STAGE}"
RAILS_HOST = os.environ[f"RAILS_HOST_{STAGE.upper().replace("-", "_")}"]
LAMBDA_API_KEY = os.environ[f"LAMBDA_API_KEY_{STAGE.upper().replace("-", "_")}"]
SQS_ARN_ROOT = os.environ["SQS_ARN_ROOT"]

# define session
aws_profile = os.getenv("AWS_PROFILE")
session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")

# define clients
s3_client = session.client("s3")
lambda_client = session.client("lambda")


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
        "-e",
        f"RAILS_HOST={RAILS_HOST}",
        "-e",
        f"LAMBDA_API_KEY={LAMBDA_API_KEY}",
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

    # create sqs event to trigger status receiver with
    event, status_receipt_handle = status_setup(subtests, TEST_STATUS_QUEUE)

    # execute lambda in local docker container
    with subtests.test(msg="execute docker lambda locally"):
        # Send a POST request to the Lambda function
        response = requests.post(LAMBDA_ENDPOINT, data=json.dumps(event), headers={"Content-Type": "application/json"})

        # print docker logs
        print_container_logs(RECEIVER_NAME)

        # check response successful, and tables / files look as they should given success
        assert response.status_code == 200
        content = json.loads(response.content.decode("utf-8"))
        assert content["statusCode"] == 500

    # delete status message
    with subtests.test(msg="delete status message"):
        delete_response = message_delete(TEST_STATUS_QUEUE, status_receipt_handle)
        assert delete_response is True
