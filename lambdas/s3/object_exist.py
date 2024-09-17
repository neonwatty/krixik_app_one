from s3 import s3_client


def exist(bucket_name: str, object_key: str):
    try:
        # Attempt to retrieve metadata for the object
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except Exception as e:
        print(f"FAILURE: object does not exist {object_key} in bucket {bucket_name} with exception {e}")
        return False
