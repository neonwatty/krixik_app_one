from aws_scaffold import session

s3_client = session.client("s3", region_name="us-west-2")


def add_lifecycle_expire(bucket_name: str, num_days: int = 1) -> bool:
    try:
        # Define the lifecycle configuration
        lifecycle_config_settings = {"Rules": [{"ID": "ExpireObjectsAfterOneDay", "Expiration": {"Days": 1}, "Status": "Enabled", "Filter": {}}]}

        # Apply the lifecycle configuration to the bucket
        s3_client.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_config_settings)

        print(f"SUCCESS: lifecycle expire rule added to bucket {bucket_name}")
        return True
    except Exception as e:
        failure_message = f"FAILURE: lifecycle expire add falied with exception {e} on bucket {bucket_name}"
        print(failure_message)
        return False
