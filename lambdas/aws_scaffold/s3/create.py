from aws_scaffold import session
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

s3_client = session.client("s3", region_name="us-west-2")


def create_bucket(bucket_name: str):
    try:
        # create bucket
        response = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "us-west-2"})
        print(f"response --> {response}")

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"SUCCESS: bucket created - {bucket_name}")
            return True

        print(f"FAILURE: bucket not created - {bucket_name}")
        return False
    except NoCredentialsError:
        print("FAILURE: credentials not available.")
        return False
    except PartialCredentialsError:
        print("FAILURE: incomplete credentials provided.")
        return False
    except ClientError as e:
        print(f"FAILURE: ClientError: {e}")
        return False
    except Exception as e:
        print(f"FAILURE: an error occurred: {e}")
        return False
