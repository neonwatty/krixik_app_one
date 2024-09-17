import pytest
import os
from tests.utilities.execute_subprocess import execute_subprocess_command

current_directory = os.getcwd()

STAGE = "test"
receivers = ["receiver_start", "receiver_preprocess", "receiver_process", "receiver_end", "receiver_status"]


@pytest.mark.parametrize("RECEIVER_NAME", receivers)
def test_build_image(RECEIVER_NAME):
    # build image
    command = ["bash", "build_image.sh", STAGE, RECEIVER_NAME]
    stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")


@pytest.mark.parametrize("RECEIVER_NAME", receivers)
def test_deploy_image(RECEIVER_NAME):
    # deploy image
    command = ["bash", "deploy_image.sh", STAGE, RECEIVER_NAME]
    stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas/build_deploy_scripts")
