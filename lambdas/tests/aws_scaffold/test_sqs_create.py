import pytest
from aws_scaffold.sqs.create import create_sqs_queue
from aws_scaffold.sqs.delete import delete_sqs_queue
import random
import time

custom_charset = "abcdefghijklmnopqrstuvwxyz"


def generate_custom_random_string(length):
    return "".join(random.choices(custom_charset, k=length))


bucket_names = [f"test-queue-{generate_custom_random_string(7)}"]


@pytest.mark.parametrize("queue_nane", bucket_names)
def test_create(queue_nane):
    create_val = create_sqs_queue(queue_nane)
    assert create_val == True


@pytest.mark.parametrize("queue_nane", bucket_names)
def test_destroy(queue_nane):
    time.sleep(5)
    destroy_val = delete_sqs_queue(queue_nane)
    assert destroy_val == True
