import os
import boto3
import json
import uuid
import time
from sqs.messages.message_create import message_create
from sqs.messages.message_poll import message_poll
from config import APP_NAME_PRIVATE, STAGE


# define session
aws_profile = os.getenv("AWS_PROFILE")
session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")

# define clients
s3_client = session.client("s3")
lambda_client = session.client("lambda")

# import variables
SQS_ARN_ROOT = os.environ["SQS_ARN_ROOT"]


# create event - nested like triggered event from s3 --> sqs
def s3sqs_event_maker(bucket_name: str, s3_key: str, queue_name: str, receipt_handle: str) -> dict:
    ## build record for triggering receiver
    # build s3 record
    bucket = {}
    bucket["name"] = bucket_name
    object = {}
    object["key"] = s3_key
    s3 = {}
    s3["bucket"] = bucket
    s3["object"] = object
    s3_record = {"s3": s3}

    # build queue record
    queue_arn = f"{SQS_ARN_ROOT}{queue_name}"

    # construct general record
    general_record = {"eventSourceARN": queue_arn, "receiptHandle": receipt_handle, "body": json.dumps({"Records": [s3_record]})}

    # construct general records holder
    event = {"Records": [general_record]}

    # construct event
    return event


def step_setup(
    subtests,
    test_file_name,
    test_file_path,
    bucket_name: str,
    receiver_queue: str,
    step: str,
    step_progress: str = "in_progress",
    file_id_override: str | None = None,
):
    # upload file file data for testing
    local_file_path = test_file_path
    upload_id = 0  # hash_file(test_file_path)
    request_id = str(uuid.uuid4())
    filename = test_file_name
    user_id = 0
    s3_key = f"{user_id}/{upload_id}/{filename}"

    # define s3_key_save based on filename
    s3_key_save = None
    if filename == "receiver_start":
        s3_key_save = f"{user_id}/{upload_id}/receiver_preprocess"
    if filename == "receiver_preprocess":
        s3_key_save = f"{user_id}/{upload_id}/receiver_process"

    # set status
    assert step in ["receiver_preprocess", "receiver_process", "receiver_end"]

    # upload test file
    with subtests.test(msg="create a test file"):
        with open(local_file_path, "rb") as file_data:
            s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=file_data)

    # create message in queue, poll for receipt to pass
    message_id = None
    receipt_handle = None

    ### upload first time --> for successful completion ###
    # create message
    with subtests.test(msg="create test message"):
        response = message_create(receiver_queue, {})
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        message_id = response["MessageId"]

    # poll for message to get receipt
    with subtests.test(msg="poll for test message receipt"):
        receipt_handle = message_poll(receiver_queue, message_id)
        assert receipt_handle is not None

    # sleep to let setup complete
    time.sleep(2)
    return upload_id, request_id, s3_key, s3_key_save, receipt_handle


def status_setup(subtests, status_queue: str):
    ### upload first time --> for successful completion ###
    # create message
    with subtests.test(msg="create test message"):
        response = message_create(status_queue, {})
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        message_id = response["MessageId"]

    # poll for message to get receipt
    with subtests.test(msg="poll for test message receipt"):
        receipt_handle = message_poll(status_queue, message_id)
        assert receipt_handle is not None

    # build status
    test_status = {"lambda": "receiver_start", "user_id": 1, "upload_id": 1, "status": "complete"}

    # build queue record
    queue_arn = f"{SQS_ARN_ROOT}{status_queue}"

    # construct general record
    general_record = {"eventSourceARN": queue_arn, "receiptHandle": receipt_handle, "body": json.dumps(test_status)}

    # construct general records holder
    event = {"Records": [general_record]}
    return event, receipt_handle
