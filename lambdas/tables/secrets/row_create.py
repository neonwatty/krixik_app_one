from tables.secrets import dynamodb_resource
from tables.secrets import table_name
from tables.secrets import generate_api_key
from datetime import datetime, timezone


def create(user_id: str, api_id: str):
    # try to update api_id
    try:
        # Get table based on table_name
        table = dynamodb_resource.Table(table_name)

        # load attribute values and expression
        attribute_value = {}
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())
        attribute_expression = "SET created_at = :createdAtValue, last_updated = :lastUpdatedValue,  api_id = :apiIdValue, api_key = :apiKeyValue"
        attribute_values = {}
        attribute_values[":createdAtValue"] = timestamp
        attribute_values[":lastUpdatedValue"] = timestamp
        attribute_values[":apiIdValue"] = api_id
        attribute_values[":apiKeyValue"] = generate_api_key()

        # update item
        response = table.update_item(
            Key={"user_id": user_id}, UpdateExpression=attribute_expression, ExpressionAttributeValues=attribute_values, ReturnValues="NONE"
        )

        print("SUCCESS: secrets update ran successfully")

    except Exception as e:
        print(f"FAILURE: secrets update failed with exception: {e}")
        raise e
