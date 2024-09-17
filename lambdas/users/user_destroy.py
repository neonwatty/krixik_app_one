from tables.public.row_destroy import destroy as public_destroy_row
from tables.secrets.row_delete import delete as secrets_row_delete


def handler(event, context):
    # check that user_id is in event
    assert "user_id" in event, "user_id not in event"
    assert event["user_id"] is not None, "user_id is None"
    user_id = event["user_id"]

    try:
        # add new user to user_ledger
        table_name = "user-ledger"
        public_destroy_row(table_name, "id", user_id)

        # write new row to secrets
        secrets_row_delete(user_id)

        success_message = "SUCCESS: user_destroy succeeded"
        print(success_message)
        return {
            "statusCode": 200,
            "body": success_message,
        }

    except Exception as e:
        failure_message = f"FAILURE: user_destroy failed with exception {e}"
        print(failure_message)
        return {"statusCode": 500, "body": failure_message}
