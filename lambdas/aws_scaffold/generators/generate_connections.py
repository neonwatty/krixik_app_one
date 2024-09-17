from aws_scaffold.s3.add_event import configure_s3_bucket_notification
from aws_scaffold.s3.add_lifecycle import add_lifecycle_expire
from aws_scaffold.sqs.attach_policy import attach_policy_to_sqs_queue


def create_single_connection(record: dict) -> bool:
    # unpack
    bucket = record["bucket"]
    expire = record["expire"]
    events = record["events"]

    # check expire
    if expire is True:
        # add expire lifecycle policy to bucket
        val = add_lifecycle_expire(bucket)
        if val is False:
            print(f"FAILURE: failed to add expire policy to bucket {bucket}")
            return False

    # check events
    if events is not None:
        # loop over events, add adjustment to queue first
        for event in events:
            queue = event["queue"]
            suffix = event["suffix"]

            # step 1: add adjustment to queue
            val = attach_policy_to_sqs_queue(queue, bucket)
            if val is False:
                print(f"FAILURE: failed to attach policy to queue {queue} for invokation by bucket {bucket}")
                return False

            # step 2: configure s3 to emit events to queue
            val = configure_s3_bucket_notification(bucket, queue, suffix)
            if val is False:
                print(f"FAILURE: failed to add event policy to bucket {bucket} for queue receiver {queue}")
                return False
    return True


def create_connections(all_records: list) -> bool:
    try:
        # loop over each record and invoke appropriate adjustmnent function
        for record in all_records:
            val = create_single_connection(record)
            if val is False:
                print("FAILURE: create_connections failed")
                return False

        # complete
        print("SUCCESS: create_connections completed successfully")
        return True
    except Exception as e:
        print(f"FAILURE: create_connections failed with exception {e}")
        return False
