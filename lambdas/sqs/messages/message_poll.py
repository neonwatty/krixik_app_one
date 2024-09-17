import json
import time
from sqs.messages import sqs_client


def message_poll_no_id(queue_name: str) -> dict | None:
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        # Poll the queue
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,  # Get only one message at a time
            WaitTimeSeconds=5,  # Long polling
        )

        messages = response.get("Messages", [])

        if messages:
            # Retrieve the first message
            message = messages[0]
            receipt_handle = message["ReceiptHandle"]

            # Delete the message from the queue
            sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

            # Return the message content or details if needed
            return {"message_id": message["MessageId"], "message": json.loads(message["Body"]), "receipt_handle": receipt_handle}

        # Increment attempt counter and wait before the next poll
        attempt += 1
        time.sleep(5)

    # Return None if no messages were found after the maximum number of attempts
    return None


def message_poll(queue_name: str, target_message_id: str) -> dict | None:
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        # Poll the queue
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,  # Adjust based on your needs
            WaitTimeSeconds=5,  # Long polling
        )

        if "Messages" in response:
            for message in response["Messages"]:
                if message.get("MessageId") == target_message_id:
                    sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
                    return message["ReceiptHandle"]

        # Increment attempt counter and wait before next poll
        attempt += 1
        time.sleep(5)
