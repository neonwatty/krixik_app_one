from tables.gateway import dynamodb_resource
from tables.gateway import table_name
from datetime import datetime, timezone


def create(api_id: str, resource_arns: list) -> None:
    try:
        # Create a timestamp
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())

        # Get the DynamoDB table
        table = dynamodb_resource.Table(table_name)

        # Update the item based on the key value
        table.update_item(
            Key={
                "api_id": api_id  # Specify the key attribute name and value
            },
            UpdateExpression="SET #methodAttr = :methodValue, #createdAt = :createdAtValue, #lastUpdated = :lastUpdatedValue",
            ExpressionAttributeNames={
                "#methodAttr": "resource_arns",
                "#createdAt": "created_at",
                "#lastUpdated": "last_updated",
            },
            ExpressionAttributeValues={":methodValue": resource_arns, ":createdAtValue": timestamp, ":lastUpdatedValue": timestamp},
            ReturnValues="NONE",  # Can be changed to "ALL_NEW" to return the updated item
        )

        print("SUCCESS: create gateway row succeeded")
    except Exception as e:
        print(f"FAILURE: create gareway row failed with exception {e}")
        raise e
