from aws_scaffold import session
from botocore.exceptions import ClientError

sqs_client = session.client("sqs", region_name="us-west-2")


def delete_sqs_queue(queue_url: str) -> bool:
    try:
        # Delete the queue
        sqs_client.delete_queue(QueueUrl=queue_url)
        print(f"SUCCESS: Queue with URL '{queue_url}' deleted successfully.")
        return True
    except ClientError as e:
        print(f"FAILURE: ClientError: {e}")
        return False
    except Exception as e:
        print(f"FAILURE: An error occurred: {e}")
        return False
