import os
from aws_scaffold import APP_NAME_PRIVATE

# define connected stages
connected_stages = ["test", "development", "production"]

# define decoupled stages
decoupled_stage = "test-decoupled"

# define receiver names for s3-queue connecitons
receiver_names = ["receiver_status", "receiver_preprocess", "receiver_process", "receiver_end"]


def generate_bucket_names() -> tuple:
    # generate s3 bucket names for connected stages
    main_bucket_names = []
    main_host_names = []
    trigger_bucket_names = []
    for stage in connected_stages:
        main_bucket_names += [f"{APP_NAME_PRIVATE}-{stage}"]
        main_host_names += [os.environ[f"RAILS_HOST_{stage.upper()}"]]
        trigger_bucket_names += [f"{APP_NAME_PRIVATE}-trigger-{stage}"]
    all_bucket_names = main_bucket_names + trigger_bucket_names

    # add host names to main buckets for cors
    bucket_host_pairs = []
    for a, b in zip(main_bucket_names, main_host_names):
        bucket_host_pairs += [a, b]

    # generate decoupled s3 bucket names
    all_bucket_names += [f"{APP_NAME_PRIVATE}-trigger-{decoupled_stage}"]

    # create app integration test data bucket
    all_bucket_names += [f"{APP_NAME_PRIVATE}-integration-test-data"]

    # add serverless directory to list
    all_bucket_names += [f"{APP_NAME_PRIVATE}-serverless-artifacts"]
    return all_bucket_names, bucket_host_pairs


def generate_queue_names() -> list:
    queue_names = []
    for receiver_name in receiver_names:
        for stage in connected_stages + [decoupled_stage]:
            queue = f"{APP_NAME_PRIVATE}-{receiver_name}-{stage}"
            queue_names.append(queue)
    return queue_names


def generate_connection_records() -> list:
    # instantiate all records container
    all_records = []

    # create record for test-decoupled bucket
    record = {}
    record["bucket"] = f"{APP_NAME_PRIVATE}-trigger-{decoupled_stage}"
    record["expire"] = True
    record["events"] = None
    all_records.append(record)

    # create record for integration test bucket
    record = {}
    record["bucket"] = f"{APP_NAME_PRIVATE}-integration-test-data"
    record["expire"] = True
    record["events"] = None
    all_records.append(record)

    # records for un-connected buckets (carriers for stages)
    record = {}
    record["bucket"] = f"{APP_NAME_PRIVATE}-test"
    record["expire"] = True
    record["events"] = None
    all_records.append(record)

    record = {}
    record["bucket"] = f"{APP_NAME_PRIVATE}-development"
    record["expire"] = False
    record["events"] = None
    all_records.append(record)

    record = {}
    record["bucket"] = f"{APP_NAME_PRIVATE}-production"
    record["expire"] = False
    record["events"] = None
    all_records.append(record)

    # records for queue connected buckets
    for stage in connected_stages:
        record = {}
        record["bucket"] = f"{APP_NAME_PRIVATE}-trigger-{stage}"
        record["expire"] = True
        record["events"] = [
            {"queue": f"{APP_NAME_PRIVATE}-receiver_preprocess-{stage}", "suffix": "receiver_start"},
            {"queue": f"{APP_NAME_PRIVATE}-receiver_process-{stage}", "suffix": "receiver_preprocess"},
            {"queue": f"{APP_NAME_PRIVATE}-receiver_end-{stage}", "suffix": "receiver_process"},
        ]
        all_records.append(record)
    return all_records
