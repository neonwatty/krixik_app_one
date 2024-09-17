from aws_scaffold import session
from botocore.exceptions import ClientError

ecr_client = session.client("ecr", region_name="us-west-2")


def create_ecr_repository(repository_name: str) -> bool:
    try:
        response = ecr_client.create_repository(repositoryName=repository_name)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"SUCCESS: Repository '{repository_name}' created successfully.")
            return True
        return False
    except ClientError as e:
        print(f"FAILURE: ClientError: {e}")
        return False
    except Exception as e:
        print(f"FAILURE: An error occurred: {e}")
        return False
