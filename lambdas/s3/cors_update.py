from s3 import s3_client
from botocore.exceptions import ClientError


def update(bucket_name: str, host_name: str) -> bool:
    # Define the new CORS configuration
    cors_configuration = {
        "CORSRules": [
            {
                "AllowedHeaders": ["Content-Type", "Content-MD5", "Content-Disposition"],
                "AllowedMethods": [
                    "PUT"
                    # "GET",
                    # "POST"
                ],
                "AllowedOrigins": [host_name],
                "ExposeHeaders": [],
                "MaxAgeSeconds": 3600,
            }
        ]
    }

    # Apply the new CORS configuration to the bucket
    try:
        s3_client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
        print(f"SUCCESS: CORS configuration successfully updated for bucket: {bucket_name}")
        return True
    except ClientError as e:
        print(f"FAILURE: Error updating CORS configuration: {e}")
        return False
