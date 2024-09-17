from tables.public import supabase_client


def create(table_name: str, key: str, value: str, document: dict = {}) -> bool:
    try:
        document[key] = value
        response = supabase_client.table(table_name).insert(document).execute()
        print("SUCCESS: create ran successfully")
        return True
    except Exception as e:
        failure_message = f"FAILURE: create failed with exception {e}"
        print(failure_message)
        raise ValueError(failure_message)
