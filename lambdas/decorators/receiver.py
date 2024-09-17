import os
import json
from sqs.messages.message_create import message_create
from sqs.messages.message_delete import message_delete
from functools import wraps
from receivers.utilities.setup_teardown import receiver_setup, receiver_teardown

STAGE = os.environ["STAGE"]
APP_NAME_PRIVATE = os.environ["APP_NAME_PRIVATE"]
RECEIVER_NAME = os.environ["RECEIVER_NAME"]
STATUS_QUEUE = f"{APP_NAME_PRIVATE}-receiver_status-{STAGE}"


def receiver_decorator(local_input_ext, local_output_ext):
    def decorator(receiver):
        @wraps(receiver)
        def wrapper(event, context):
            try:
                ### unpack message from sqs queue ####
                # Unpack records
                if "Records" not in event:
                    raise KeyError("No 'records' found in the event")
                records = event.get("Records", [])
                general_record = records[0]

                if "eventSourceARN" not in general_record:
                    raise KeyError("No 'eventSourceARN' found in general_record")
                queue_arn = general_record["eventSourceARN"]

                if "receiptHandle" not in general_record:
                    raise KeyError("No 'receiptHandle' found in general_record")
                receipt_handle = general_record["receiptHandle"]

                # unpack queue_name and s3 record data
                queue_name = queue_arn.split(":")[-1]
                s3_record = json.loads(general_record["body"])["Records"][0]

                ### setup data, download object from s3 ###
                # setup - download input from s3
                setup_payload = receiver_setup(RECEIVER_NAME, s3_record, local_input_ext, local_output_ext)

                # run function
                receiver_response = receiver(setup_payload, {})

                # teardown - upload output to s3
                s3_key_save = receiver_teardown(setup_payload)

                # delete receiver input message
                del_message_val = message_delete(queue_name, receipt_handle)

                ### route status update message ###
                status = {"lambda": RECEIVER_NAME, "user_id": setup_payload["user_id"], "upload_id": setup_payload["upload_id"], "status": "complete"}
                if receiver_response["statusCode"] != 200:
                    status["status"] = "failed"
                else:  # load up receiver_response with location metadata
                    receiver_response["body"]["s3_key_save"] = s3_key_save
                    receiver_response["body"]["bucket_name_save"] = setup_payload["s3_bucket"]

                # send message to queue
                status_response = message_create(STATUS_QUEUE, status)

                # return receiver response
                return receiver_response

            except Exception as e:
                failure_message = f"BAD REQUEST: failure in processing {e}"
                print(failure_message)
                return {
                    "statusCode": 500,
                    "body": json.dumps(failure_message),
                }

        return wrapper

    return decorator
