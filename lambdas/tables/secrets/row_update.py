from tables.secrets import dynamodb_resource
from tables.secrets import table_name
from tables.secrets.row_read import read
from tables.secrets.row_create import create
from tables.secrets import generate_api_key
from datetime import datetime, timezone


def update(user_id: str, api_id: str = "", api_key: bool = False) -> None:
    try:
        table = dynamodb_resource.Table(table_name)
        response = read(user_id)
        if "Item" in response:
            timestamp = int(datetime.now(tz=timezone.utc).timestamp())
            attribute_expression = "SET last_updated = :lastUpdatedValue"
            attribute_values = {}
            attribute_values[":lastUpdatedValue"] = timestamp

            if len(api_id) > 0:
                attribute_expression += ", api_id = :apiIdValue"
                attribute_values[":apiIdValue"] = api_id
            if api_key is True:
                attribute_expression += ", api_key = :apiKeyValue"
                attribute_values[":apiKeyValue"] = generate_api_key()

            response = table.update_item(
                Key={"user_id": user_id}, UpdateExpression=attribute_expression, ExpressionAttributeValues=attribute_values, ReturnValues="NONE"
            )
        else:
            if len(api_id) > 0:
                create(user_id, api_id)
            else:
                raise ValueError(f"FAILURE: secrets ledger update row failed - null api_id")
        print("SUCCESS: secrets update ran successfully")

    except Exception as e:
        print(f"FAILURE: secrets update failed with exception: {e}")
        raise e
