from s3 import s3_client


def list_subdir(bucket_name: str, subdir_prefix: str) -> list:
    subdir_file_list = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=subdir_prefix).get("Contents", [])
    return subdir_file_list


def upload(bucket_name: str, local_file_path: str, object_key: str) -> bool:
    try:
        # Upload the local file to S3
        s3_client.upload_file(local_file_path, bucket_name, object_key)
        print(f"SUCCESS: uploaded {local_file_path} to s3://{bucket_name}/{object_key}")
        return True
    except Exception as e:
        failure_message = f"FAILURE: s3 upload failed with exception {e}"
        print(failure_message)
        return False


def download(bucket_name: str, object_key: str, local_file_path: str) -> bool:
    try:
        # Download the object from S3
        s3_client.download_file(bucket_name, object_key, local_file_path)
        print(f"SUCCESS: downloaded {object_key} to {local_file_path}")
        return True
    except Exception as e:
        failure_message = f"FAILURE: s3 download failed with exception {e}"
        print(failure_message)
        return False


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
