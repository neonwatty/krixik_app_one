from s3 import s3_client


def list_subdir(bucket_name: str, subdir_prefix: str) -> list:
    subdir_file_list = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=subdir_prefix).get("Contents", [])
    return subdir_file_list


def delete_subdir(bucket_name: str, subdir_prefix: str) -> None:
    try:
        # create subdir file list
        subdir_file_list = list_subdir(bucket_name, subdir_prefix)

        # loop over files in list and delete
        for obj in subdir_file_list:
            s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])

        # Delete the subdirectory (if desired)
        # Note: S3 does not have a concept of directories, so this step is optional
        s3_client.delete_object(Bucket=bucket_name, Key=subdir_prefix)
        print(f"SUCCESS: deleted subdirectory: {subdir_prefix}")
    except Exception as e:
        failure_message = f"FAILURE: s3 delete user file subdir failed with exception: {e}"
        print(failure_message)
        raise e
