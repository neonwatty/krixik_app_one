import os
from receivers import s3_client
from sqs.messages.message_create import message_create
from decorators.warmer import warmer
from receivers.utilities.create_io_dir import local_input_file_path

APP_NAME_PRIVATE = os.environ["APP_NAME_PRIVATE"]
STAGE = os.environ["STAGE"]
STATUS_QUEUE = f"{APP_NAME_PRIVATE}-receiver_status-{STAGE}"
BUCKET_NAME_SAVE = f"{APP_NAME_PRIVATE}-trigger-{STAGE}"


@warmer
def lambda_handler(event, context):
    try:
        # Parse the JSON payload
        message = event["message"]
        file_key = event["file_key"]
        bucket_name = event["bucket_name"]
        stage = event["stage"]
        user_id = event["user_id"]
        upload_id = event["upload_id"]

        # download file to lambda
        s3_client.download_file(bucket_name, file_key, local_input_file_path)
        print(f"SUCCESS: File downloaded to {local_input_file_path}")

        # save file back to s3
        s3_key_save = f"{user_id}/{upload_id}/receiver_start"
        s3_client.upload_file(local_input_file_path, BUCKET_NAME_SAVE, s3_key_save)
        print("SUCCESS: File uploaded to s3")

        # send status update to queue
        status = {"lambda": "receiver_start", "user_id": user_id, "upload_id": upload_id, "status": "complete"}
        response = message_create(STATUS_QUEUE, status)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            success_message = "SUCCESS: receiver_start executed successfully"
            return {
                "statusCode": 200,
                "body": {"status": "success", "message": success_message, "s3_key_save": s3_key_save, "bucket_name_save": BUCKET_NAME_SAVE},
            }
        else:
            failure_message = f"sqs status queue did not accept status message --> {STATUS_QUEUE}"
            print(f"FAILURE: status code --> {500}")
            print(failure_message)
            return {"statusCode": 500, "body": {"status": "error", "message": failure_message}}
    except Exception as e:
        try:
            # send status update to queue
            status = {"lambda": "receiver_start", "user_id": user_id, "upload_id": upload_id, "status": "fail"}
            response = message_create(STATUS_QUEUE, status)
        except:  # noqa E722
            pass

        failure_message = str(e)
        print(f"FAILURE: status code --> {500}")
        print(failure_message)
        return {"statusCode": 500, "body": {"status": "error", "message": failure_message}}
