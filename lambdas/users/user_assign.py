import random
from tables.gateway.row_read import get_all_api_ids
from tables.secrets.row_delete import delete
from tables.secrets.row_create import create


def assign_gateway(user_id: str):
    try:
        # delete user's current api_id assigment
        delete(user_id)

        # collect all gateways
        api_ids = get_all_api_ids("gateway-ledger")

        # choose a random api_id
        user_api_id = random.choice(api_ids)

        # write new row to secrets
        create(user_id, user_api_id)
        print("SUCCESS: assign_gateway succeeded")
    except Exception as e:
        failure_message = f"FAILURE: failed with exception {e}"
        print(failure_message)
        raise e
