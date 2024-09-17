from aws_scaffold import session
from botocore.exceptions import ClientError

s3_client = session.client("s3", region_name="us-west-2")


def delete_bucket(bucket_name: str):
    try:
        # Now delete the bucket itself
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"SUCCESS: bucket '{bucket_name}' deleted successfully.")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"FAILURE: bucket '{bucket_name}' does not exist.")
            return False
        elif e.response["Error"]["Code"] == "NoSuchBucket":
            print(f"FAILURE: bucket '{bucket_name}' does not exist or has already been deleted.")
            return False
        elif e.response["Error"]["Code"] == "BucketNotEmpty":
            print(f"FAILURE: bucket '{bucket_name}' is not empty. Ensure all objects are deleted before trying again.")
            return False
        else:
            print(f"FAILURE: ClientError: {e}")
            return False
    except Exception as e:
        print(f"FAILURE: an error occurred: {e}")
        return False
