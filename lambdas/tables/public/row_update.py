from tables.public import supabase_client


def update(table_name: str, key: str, value: str, document: dict) -> bool:
    try:
        response = supabase_client.table(table_name).update(document).eq(key, value).execute()
        print("SUCCESS: update ran successfully")
        return True
    except Exception as e:
        failure_message = f"FAILURE: update failed with exception {e}"
        print(failure_message)
        raise ValueError(failure_message)
