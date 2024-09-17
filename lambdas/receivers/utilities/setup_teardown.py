from receivers import s3_client
from receivers.utilities.create_io_dir import local_input_file_path, local_output_file_path


def receiver_setup(receiver_name: str, event: dict, local_input_ext: str | None = None, local_output_ext: str | None = None) -> dict | None:
    try:
        if receiver_name == "receiver_status":
            setup_payload = {}
            setup_payload["message"] = event["message"]
            return setup_payload
        else:
            # unpack required objects from event
            s3_bucket = event["s3"]["bucket"]["name"]
            s3_key = event["s3"]["object"]["key"]

            # deconstruct s3_key into stage, user_id, file_id, and file_name
            s3_key_split = s3_key.split("/")
            user_id = s3_key_split[0]
            upload_id = s3_key_split[1]
            file_name = s3_key_split[2]

            # adjust local_input_file_path for function to work properly
            local_input_path = local_input_file_path + local_input_ext if local_input_ext is not None else local_input_file_path
            local_output_path = local_output_file_path + local_output_ext if local_output_ext is not None else local_output_file_path

            # Download the image from S3
            if receiver_name != "receiver_end":
                s3_client.download_file(s3_bucket, s3_key, local_input_path)

            # return setup payload
            setup_payload = {}
            setup_payload["user_id"] = user_id
            setup_payload["upload_id"] = upload_id
            setup_payload["local_input_path"] = local_input_path
            setup_payload["local_output_path"] = local_output_path
            setup_payload["s3_bucket"] = s3_bucket
            setup_payload["s3_key"] = s3_key
            setup_payload["receiver_name"] = receiver_name
            return setup_payload
    except Exception as e:
        failure_message = f"FAILURE: setup for event {event} failed with exception {str(e)}"
        print(failure_message)
        return None


def receiver_teardown(setup_payload: dict) -> str | None:
    try:
        # delete old file
        s3_client.delete_object(Bucket=setup_payload["s3_bucket"], Key=setup_payload["s3_key"])

        # upload file if not at receiver end
        if setup_payload["receiver_name"] != "receiver_end":
            # save new file
            s3_key_save = f"{setup_payload["user_id"]}/{setup_payload["upload_id"]}/{setup_payload["receiver_name"]}"
            s3_client.upload_file(setup_payload["local_output_path"], setup_payload["s3_bucket"], s3_key_save)
            return s3_key_save
        else:
            return "no file to upload"
    except Exception as e:
        failure_message = f"FAILURE: teardown for receiver {setup_payload["receiver_name"]} failed with exception {str(e)}"
        print(failure_message)
        return None
