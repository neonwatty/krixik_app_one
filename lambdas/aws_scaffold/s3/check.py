from aws_scaffold import session
from botocore.exceptions import ClientError

s3_client = session.client("s3", region_name="us-west-2")


def bucket_exists(bucket_name: str):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"SUCCESS: bucket_exist check passed for {bucket_name}")
        return True
    except ClientError as e:
        # Check if the error is because the bucket does not exist
        if e.response["Error"]["Code"] == "404":
            print(f"FAILURE: bucket '{bucket_name}' does not exist.")
            return False
        else:
            print(f"FAILURE: clientError: {e}")
        return False
    except Exception as e:
        print(f"FAILURE: an error occurred: {e}")
        return False
