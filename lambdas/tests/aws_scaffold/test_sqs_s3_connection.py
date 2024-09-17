import pytest
from aws_scaffold.s3.create import create_bucket
from aws_scaffold.s3.delete import delete_bucket
from aws_scaffold.sqs.create import create_sqs_queue
from aws_scaffold.sqs.delete import delete_sqs_queue
from aws_scaffold.sqs.attach_policy import attach_policy_to_sqs_queue
from aws_scaffold.s3.add_event import configure_s3_bucket_notification
import random

custom_charset = "abcdefghijklmnopqrstuvwxyz"


def generate_custom_random_string(length):
    return "".join(random.choices(custom_charset, k=length))


# create test bucket_name, queue_name, and suffix
bucket_name = f"test-bucket-{generate_custom_random_string(7)}"
queue_name = f"test-queue-{generate_custom_random_string(7)}"
suffix = "marymother"


# create bucket
def test_create_bucket():
    val = create_bucket(bucket_name)
    assert val == True


# create queue
def test_create_queue():
    val = create_sqs_queue(queue_name)
    assert val == True


# create connection between them
def test_attach_policy_to_sqs():
    val = attach_policy_to_sqs_queue(queue_name, bucket_name)
    if val is not True:
        destroy_val = delete_bucket(bucket_name)
        assert destroy_val == True

        destroy_val = delete_sqs_queue(queue_name)
        assert destroy_val == True
    assert val == True


# add s3 object created event trigger s3 to send suffix-filtered created files to sqs queue
def test_add_event():
    val = configure_s3_bucket_notification(bucket_name, queue_name, suffix)
    if val is not True:
        destroy_val = delete_bucket(bucket_name)
        assert destroy_val == True

        destroy_val = delete_sqs_queue(queue_name)
        assert destroy_val == True
    assert val is True


# # destroy bucket and queue
# def destroy_bucket_and_queue():
#     destroy_val = delete_bucket(bucket_name)
#     assert destroy_val == True

#     destroy_val = delete_sqs_queue(queue_name)
#     assert destroy_val == True
