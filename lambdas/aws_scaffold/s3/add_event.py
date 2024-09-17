from aws_scaffold import session, ACCOUNT_ID
from botocore.exceptions import ClientError


s3_client = session.client("s3", region_name="us-west-2")


def get_bucket_notifications(bucket_name):
    try:
        response = s3_client.get_bucket_notification_configuration(Bucket=bucket_name)
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketNotificationConfiguration":
            return {}  # No existing notification configuration
        else:
            raise


def configure_s3_bucket_notification(bucket_name: str, queue_name: str, suffix=None) -> bool:
    # get bucket's current queue events
    current_notifications = get_bucket_notifications(bucket_name)

    # convert queue_name to arn
    queue_arn = f"arn:aws:sqs:us-west-2:{ACCOUNT_ID}:{queue_name}"

    # Define the notification configuration
    queue_configuration = {"QueueArn": queue_arn, "Events": ["s3:ObjectCreated:*"]}

    if suffix:
        queue_configuration["Filter"] = {"Key": {"FilterRules": [{"Name": "suffix", "Value": suffix}]}}

    if "QueueConfigurations" in current_notifications:
        queue_configs = current_notifications["QueueConfigurations"]
    else:
        queue_configs = []

    # Append the new queue configuration if it doesn't already exist
    if not any(q["QueueArn"] == queue_arn for q in queue_configs):
        queue_configs.append(queue_configuration)

    # Prepare the new notification configuration
    updated_notifications = {"QueueConfigurations": queue_configs}

    try:
        # Set the notification configuration
        s3_client.put_bucket_notification_configuration(Bucket=bucket_name, NotificationConfiguration=updated_notifications)
        print(f"SUCCESS: Notification configuration set for bucket '{bucket_name}' with suffix '{suffix}'.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
