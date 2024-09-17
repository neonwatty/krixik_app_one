from aws_scaffold import session
from botocore.exceptions import ClientError

ecr_client = session.client("ecr", region_name="us-west-2")


def repository_exists(repository_name, region="us-east-1"):
    try:
        # Describe the repository
        response = ecr_client.describe_repositories(repositoryNames=[repository_name])
        if response["repositories"]:
            print(f"SUCCESS: Repository '{repository_name}' exists.")
            return True
    except ClientError as e:
        # Check if the error is because the repository does not exist
        if e.response["Error"]["Code"] == "RepositoryNotFoundException":
            print(f"FAILURE: Repository '{repository_name}' does not exist.")
        else:
            print(f"FAILURE: ClientError: {e}")
        return False
    except Exception as e:
        print(f"FAILURE: An error occurred: {e}")
        return False
