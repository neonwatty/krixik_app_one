import pytest
import os
from tests.utilities.execute_subprocess import execute_subprocess_command

current_directory = os.getcwd()

STAGE = "test"

configs = ["serverless_receivers.yml"]


@pytest.mark.parametrize("config", configs)
def test_deploy(config):
    # build image
    command = ["bash", "adjust_functions.sh", "deploy", STAGE, config]
    stdout = execute_subprocess_command(command, cwd=current_directory + "/lambdas")
