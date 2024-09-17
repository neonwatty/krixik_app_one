import json
from aws_scaffold import session
from aws_scaffold import ACCOUNT_ID
from botocore.exceptions import ClientError

sqs_client = session.client("sqs", region_name="us-west-2")


def get_queue_url(queue_name: str) -> str | None:
    try:
        response = sqs_client.get_queue_url(QueueName=queue_name)
        return response.get("QueueUrl")
    except ClientError as e:
        print(f"FAILURE: ClientError: {e}")
        return None
    except Exception as e:
        print(f"FAILURE: An error occurred: {e}")
        return None


def attach_policy_to_sqs_queue(queue_name: str, bucket_name: str) -> bool:
    # Get the queue URL
    queue_url = get_queue_url(queue_name)
    if not queue_url:
        print(f"Failed to retrieve URL for queue '{queue_name}'.")
        return False

    # Define the policy template
    policy_template = {
        "Version": "2012-10-17",
        "Id": "__default_policy_ID",
        "Statement": [
            {
                "Sid": "__owner_statement",
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::{ACCOUNT_ID}:root"},
                "Action": "SQS:*",
                "Resource": f"arn:aws:sqs:us-west-2:{ACCOUNT_ID}:{queue_name}",
            },
            {
                "Sid": "S3 connection",
                "Effect": "Allow",
                "Principal": {"Service": "s3.amazonaws.com"},
                "Action": "SQS:SendMessage",
                "Resource": f"arn:aws:sqs:us-west-2:{ACCOUNT_ID}:{queue_name}",
                "Condition": {"StringEquals": {"aws:SourceAccount": ACCOUNT_ID}, "ArnLike": {"aws:SourceArn": f"arn:aws:s3:::{bucket_name}"}},
            },
        ],
    }
    policy_json = json.dumps(policy_template)

    try:
        # Attach the policy
        response = sqs_client.set_queue_attributes(QueueUrl=queue_url, Attributes={"Policy": policy_json})
        print(f"SUCCESS: Policy attached successfully to queue '{queue_name}'.")
        return True
    except ClientError as e:
        print(f"FAILURE: ClientError: {e}")
        return False
    except Exception as e:
        print(f"FAILURE: An error occurred: {e}")
        return False
