from aws_scaffold import session
from botocore.exceptions import ClientError

sqs_client = session.client("sqs", region_name="us-west-2")


def create_sqs_queue(queue_name: str) -> bool:
    # define sqs attributes
    attributes = {
        "DelaySeconds": "0",
        "MaximumMessageSize": "262144",
        "MessageRetentionPeriod": "300",
        "VisibilityTimeout": "300",
        "ReceiveMessageWaitTimeSeconds": "0",
    }

    # create queue
    try:
        # Create the queue
        response = sqs_client.create_queue(QueueName=queue_name, Attributes=attributes)

        # Get the URL of the created queue
        queue_url = response.get("QueueUrl")
        print(f"SUCCESS: Queue '{queue_name}' created successfully with URL: {queue_url}")
        return True
    except ClientError as e:
        print(f"FAILURE: ClientError: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
