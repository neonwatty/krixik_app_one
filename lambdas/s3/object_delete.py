from s3 import s3_client


def delete(bucket_name: str, object_key: str) -> bool:
    try:
        # Delete each object in the subdirectory
        response = s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 204:
            failure_message = f"FAILURE: deletion failed {bucket_name}/{object_key}"
            print(failure_message)
            return False
        print("SUCCESS: deleted file")
        return True
    except Exception as e:
        failure_message = f"FAILURE: s3 deletion failed with excetpion {e}"
        print(failure_message)
        raise e
