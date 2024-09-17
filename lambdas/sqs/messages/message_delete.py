from sqs.messages import sqs_client


def message_delete(queue_name: str, receipt_handle: dict) -> bool:
    try:
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        print("SUCCESS: deleted message from queue")
        return True
    except Exception as e:
        print(f"FAILURE: delete_message failed with exception {e}")
        return False
