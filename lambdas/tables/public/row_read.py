from tables.public import supabase_client


def read(table_name: str, key: str, value: str) -> list:
    try:
        response = supabase_client.table(table_name).select("*").eq(key, value).limit(1).execute()
        print("SUCCESS: read ran successfully")
        return response.data
    except Exception as e:
        failure_message = f"FAILURE: read failed with exception {e}"
        print(failure_message)
        raise ValueError(failure_message)
