from tables.secrets import dynamodb_resource, Key
from tables.secrets import table_name, api_id_gsi_index, api_key_gsi_index


def read(user_id: str) -> dict:
    try:
        # get table based on table_name
        table = dynamodb_resource.Table(table_name)

        # get item from table
        response = table.get_item(Key={"user_id": user_id})
        print("SUCCESS: secrets row reader succeeded")
        return response
    except Exception as e:
        print(f"FAILURE: secrets row read failed with exception: {e}")
        raise e


def read_gsi(api_id: str) -> list:
    try:
        table = dynamodb_resource.Table(table_name)
        response = table.query(IndexName=api_id_gsi_index, KeyConditionExpression=Key("api_id").eq(api_id))
        print("SUCCESS: secrets read_gsi reader ran successfully")
        return response
    except Exception as e:
        print(f"FAILURE: secrets read_gsi failed with exception: {e}")
        raise e


def read_api_key(api_key: str) -> dict | None:
    try:
        table = dynamodb_resource.Table(table_name)
        response = table.query(IndexName=api_key_gsi_index, KeyConditionExpression=Key("api_key").eq(api_key))
        items = response.get("Items", None)
        print("SUCCESS: secrets read_gsi reader ran successfully")

        if items is not None:
            return items[0]
        return None
    except Exception as e:
        print(f"FAILURE: secrets read_gsi failed with exception: {e}")
        raise e
