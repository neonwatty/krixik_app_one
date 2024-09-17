from aws_scaffold.s3.create import create_bucket
from aws_scaffold.s3.delete import delete_bucket
from aws_scaffold.sqs.create import create_sqs_queue
from aws_scaffold.sqs.delete import delete_sqs_queue


def create_buckets(bucket_names: list) -> bool:
    try:
        # run through and create all buckets
        for bucket in bucket_names:
            val = create_bucket(bucket)
            if val is False:
                print(f"FAILURE: failed to create bucket {bucket}")
                return False
            else:
                print(f"SUCCESS: created bucket {bucket}")
        print("SUCCESS: create_buckets completed successfully")
        return True
    except Exception as e:
        failure_message = f"FAILURE: create_buckets failed with exception {e}"
        print(failure_message)
        return False


def destroy_buckets(bucket_names: list) -> bool:
    try:
        # run through and create all buckets
        for bucket in bucket_names:
            val = delete_bucket(bucket)
            if val is False:
                print(f"FAILURE: failed to delete bucket {bucket}")
                return False
            else:
                print(f"SUCCESS: deleteed bucket {bucket}")
        print("SUCCESS: destroy_buckets completed successfully")
        return True
    except Exception as e:
        failure_message = f"FAILURE: destroy_buckets failed with exception {e}"
        print(failure_message)
        return False


def create_queues(queue_names: list) -> bool:
    try:
        # loop through and create each queue
        for queue in queue_names:
            val = create_sqs_queue(queue)
            if val is False:
                print(f"FAILURE: failed to create queue {queue}")
                return False
            else:
                print(f"SUCCESS: created queue {queue}")
        print("SUCCESS: create_queues succeeded")
        return True
    except Exception as e:
        failure_message = f"FAILURE: create_queues failed with exception {e}"
        print(failure_message)
        return False


def destroy_queues(queue_names: list) -> bool:
    try:
        # loop through and create each queue
        for queue in queue_names:
            val = delete_sqs_queue(queue)
            if val is False:
                print(f"FAILURE: failed to delete queue {queue}")
                return False
            else:
                print(f"SUCCESS: deleted queue {queue}")
        print("SUCCESS: destroy_queues succeeded")
        return True
    except Exception as e:
        failure_message = f"FAILURE: destroy_queues failed with exception {e}"
        print(failure_message)
        return False
