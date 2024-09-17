from tables.public import supabase_client


def destroy(table_name: str, key: str, value: str) -> bool:
    try:
        response = supabase_client.table(table_name).delete().eq(key, value).execute()
        print("SUCCESS: delete_row ran successfully")
        return True
    except Exception as e:
        failure_message = f"FAILURE: delete failed with exception {e}"
        print(failure_message)
        raise ValueError(failure_message)
