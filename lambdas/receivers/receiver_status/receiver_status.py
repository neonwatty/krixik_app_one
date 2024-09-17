import os
import json
import requests
from decorators.warmer import warmer
from sqs.messages.message_delete import message_delete


STAGE = os.environ["STAGE"]
RAILS_HOST = os.environ[f"RAILS_HOST"]
LAMBDA_API_KEY = os.environ[f"LAMBDA_API_KEY"]


def process_message(message: str) -> bool:
    try:
        # create headers
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LAMBDA_API_KEY}"}

        # create url
        rails_url = f"{RAILS_HOST}/receiver_status/update"

        # fire off request
        response = requests.post(rails_url, data=json.dumps(message), headers=headers)
        if response.status_code == 200:
            print("SUCCESS: process_message executed successfully")
            return True
        else:
            print(f"FAILURE: process_message failed and returned status code - {response.status_code}")
            print(f"FAILURE: response json --> {response.json()}")
            return False
    except Exception as e:
        failure_message = f"FAILURE: process_message failed with exception {e}"
        print(failure_message)
        return False


@warmer
def lambda_handler(event, context):
    try:
        # unpack first Record from event
        record = event["Records"][0]
        message = json.loads(record["body"])

        receipt_handle = record["receiptHandle"]
        queue_arn = record["eventSourceARN"]
        queue_name = queue_arn.split(":")[-1]

        # process message
        process_val = process_message(message)

        # delete message from sqs
        del_message_val = message_delete(queue_name, receipt_handle)

        # conditional response
        if process_val is True:
            if del_message_val is True:
                success_message = "SUCCESS: status posted and message deleted"
                print(success_message)
                return {"statusCode": 200, "body": json.dumps(success_message)}
            else:
                failure_message = "FAILURE: status posted correctly BUT message was NOT deleted"
                print(failure_message)
                return {"statusCode": 500, "body": json.dumps(failure_message)}
        else:
            return {"statusCode": 500, "body": json.dumps("FAILURE: status not updated correctly")}
    except Exception as e:
        print(f"FAILURE: status send falied on message {message} with exception {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error processing sqs message: {e}"),
        }
