from aws_scaffold import session
from botocore.exceptions import ClientError

ecr_client = session.client("ecr", region_name="us-west-2")


def delete_ecr_repository(repository_name: str) -> bool:
    try:
        # Step 1: Delete all images in the repository
        print(f"Deleting images from repository '{repository_name}'...")
        response = ecr_client.list_images(repositoryName=repository_name)
        image_ids = response["imageIds"]
        while image_ids:
            # Delete images in batches
            ecr_client.batch_delete_image(repositoryName=repository_name, imageIds=image_ids)
            response = ecr_client.list_images(repositoryName=repository_name)
            image_ids = response["imageIds"]

        print(f"All images deleted from repository '{repository_name}'.")

        # Step 2: Delete the repository
        print(f"Deleting repository '{repository_name}'...")
        ecr_client.delete_repository(repositoryName=repository_name, force=True)
        print(f"Repository '{repository_name}' deleted successfully.")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "RepositoryNotEmptyException":
            print(f"Repository '{repository_name}' is not empty. Please ensure all images are deleted before trying again.")
        elif e.response["Error"]["Code"] == "RepositoryNotFoundException":
            print(f"Repository '{repository_name}' does not exist or has already been deleted.")
        else:
            print(f"ClientError: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
