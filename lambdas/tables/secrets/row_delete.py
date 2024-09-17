from tables.secrets import dynamodb_resource
from tables.secrets import table_name


def delete(user_id: str) -> None:
    try:
        # get table
        table = dynamodb_resource.Table(table_name)

        # delete row
        table.delete_item(Key={"user_id": user_id})

        # wait for row with api_id to be deleted
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        print("SUCCESS: delete secrets row executed successfully")
    except Exception as e:
        print(f"FAILURE: delete secrets row failed with exception: {e}")
        raise e
