import os
import requests
from s3.object_add import add


# this function is just for testing
def upload(user_id: str, file_id: str, filepath: str, bucket_name: str | None = None, stage: str = "dev"):
    # check that filename exists
    if not os.path.isfile(filepath):
        raise ValueError(f"FAILURE: filepath does not exist to add to s3 bucket - {filepath}")

    # create filename from filepath
    filename = filepath.split("/")[-1]

    # create presigned
    presigned_post_url_results = add(user_id, file_id, filename, bucket_name, stage)

    # unapck presigned
    url = presigned_post_url_results["url"]
    fields = presigned_post_url_results["fields"]

    # upload file
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f)}
        try:
            post_response = requests.post(url, data=fields, files=files, timeout=120)
        except Exception as e:
            raise e
        return post_response
