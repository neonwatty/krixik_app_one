from tables.public.row_read import read


def exist(table_name: str, key: str, value: str) -> bool:
    try:
        response = read(table_name, key, value)
        print("SUCCESS: read ran successfully")
        if len(response) > 0:
            return True
        return False
    except Exception as e:
        failure_message = f"FAILURE: read failed with exception {e}"
        print(failure_message)
        raise e
