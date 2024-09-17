import os
import sys
import argparse
from tests.utilities.execute_subprocess import execute_subprocess_command
from dotenv import load_dotenv

# use env file from base directory - above lambdas
current_directory = os.getcwd()
print(f"INFO: current_directory: {current_directory}")
dotenv_path = os.path.abspath(os.path.join(current_directory, "..", ".env"))
print(f"INFO: dotenv path: {dotenv_path}")
load_dotenv(dotenv_path)

stages = ["test", "test-decoupled", "development", "production"]


def deploy_receives(stage: str = "development"):
    # receiver list
    receivers = ["receiver_start", "receiver_preprocess", "receiver_process", "receiver_end", "receiver_status"]

    # build and deploy image for each receiver
    for receiver_name in receivers:
        # build image
        print(f"INFO: building image for receiver {receiver_name}")
        command = ["bash", "build_image.sh", stage, receiver_name]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")
        print("INFO: ...done!")

        # deploy image
        print(f"INFO: deploying image for receiver {receiver_name} and stage {stage}")
        command = ["bash", "deploy_image.sh", stage, receiver_name]
        stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")
        print("INFO: ...done!")

    # deploy serverless config for receivers
    config = "serverless_receivers.yml"
    print(f"INFO: deploying services in {config} to stage {stage}")
    command = ["bash", "adjust_functions.sh", "deploy", stage, config]
    stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas")
    print("INFO: ...done!")

    # prepare to update cors policy on bucket
    if stage != "test-decoupled":
        from s3.cors_update import update as cors_update

        print(f"aws_profile --> {os.environ["AWS_PROFILE"]}")

        bucket_to_update = f"{os.environ["APP_NAME_PRIVATE"]}-{stage}"
        print(f"bucket_to_update --> {bucket_to_update}")

        host_name = os.environ[f"RAILS_HOST_{stage.upper()}"]
        print(f"host_name --> {host_name}")

        val = cors_update(bucket_to_update, host_name)
        assert val is True, f"FAILURE: failed to update cors on bucket {bucket_to_update}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("stage", type=str, help="stage argument - development, test, or production")
    args = parser.parse_args()
    if args.stage not in stages:
        print(f"FAILURE: input stage {args.stage} - available stages are {stages}")
        sys.exit(1)
    deploy_receives(args.stage)
