from tables.gateway import dynamodb_resource
from tables.gateway import table_name


def delete(api_id: str) -> None:
    try:
        # get table
        table = dynamodb_resource.Table(table_name)

        # delete row
        table.delete_item(Key={"api_id": api_id})

        # wait for row with api_id to be deleted
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        print("SUCCESS: delete gateway ledger row executed successfully")
    except Exception as e:
        print(f"FAILURE: delete gateway ledger row failed with exception: {e}")
        raise e
