import json
from sqs.messages import sqs_client


def message_create(queue_name: str, payload: dict) -> dict:
    try:
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
        response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(payload))

        print(f"SUCCESS: message sent to queue_name {queue_name}")
        return response
    except Exception as e:
        fail_message = f"FAILURE: message create failed for queue_name {queue_name} with exception {e}"
        print(fail_message)
        raise ValueError(fail_message)
