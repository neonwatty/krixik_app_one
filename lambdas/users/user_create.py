from tables.validators.user_ledger import validator as user_input_validator
from tables.public.row_create import create as public_create_row
from users.user_assign import assign_gateway
import uuid


def handler(event, context):
    # check that email is in event
    assert "email" in event, "email not in event"
    assert event["email"] is not None, "email is None"
    email = event["email"]

    try:
        # create user_id
        user_id = str(uuid.uuid4())

        # validate email
        payload = {"id": user_id, "email": email}
        user_input_validator(payload)

        # add new user to user-ledger
        table_name = "user-ledger"
        key = "id"
        value = user_id
        public_create_row(table_name, key, value, {"email": email})

        # assign gateway to user
        assign_gateway(user_id)

        # print success
        success_message = "SUCCESS: create new user succeeded"
        print(success_message)
        return {"statusCode": 200, "body": success_message, "user_id": user_id}

    except Exception as e:
        failure_message = f"FAILURE: create_user failed with exception {e}"
        print(failure_message)
        return {"statusCode": 500, "body": failure_message, "user_id": None}
