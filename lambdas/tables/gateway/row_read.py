from tables.gateway import dynamodb_resource
from tables.gateway import table_name


def read(api_id: str) -> dict:
    try:
        # get table based on table_name
        table = dynamodb_resource.Table(table_name)

        # get item from table
        response = table.get_item(Key={"api_id": api_id})
        print("SUCCESS: authorizer succeeded")
        return response
    except Exception as e:
        print(f"FAILURE: gateway row read failed with exception {e}")
        raise e


def get_all_api_ids(table_name: str) -> list:
    try:
        # Get table based on table_name
        table = dynamodb_resource.Table(table_name)

        # Scan the table to retrieve all items
        response = table.scan()

        # Extract all api_ids from the items
        api_ids = [item.get("api_id") for item in response.get("Items", [])]

        print("SUCCESS: Retrieved all api_ids")
        return api_ids
    except Exception as e:
        print(f"FAILURE: Failed to retrieve api_ids with exception {e}")
        raise e
