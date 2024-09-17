import functools


def warmer(handler_func):
    @functools.wraps(handler_func)
    def wrapper(event, context):
        if event.get("source") == "warmer-test-dev-handler":
            print("WarmUp - Lambda is warm!")
            return {}
        return handler_func(event, context)

    return wrapper
