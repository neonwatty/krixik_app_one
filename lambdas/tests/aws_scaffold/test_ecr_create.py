import pytest
from aws_scaffold.ecr.create import create_ecr_repository
from aws_scaffold.ecr.delete import delete_ecr_repository
import random
import time

custom_charset = "abcdefghijklmnopqrstuvwxyz"


def generate_custom_random_string(length):
    return "".join(random.choices(custom_charset, k=length))


bucket_names = [f"test-repository-{generate_custom_random_string(7)}"]


@pytest.mark.parametrize("repository_name", bucket_names)
def test_create(repository_name):
    create_val = create_ecr_repository(repository_name)
    assert create_val == True


@pytest.mark.parametrize("repository_name", bucket_names)
def test_destroy(repository_name):
    time.sleep(5)
    destroy_val = delete_ecr_repository(repository_name)
    assert destroy_val == True
