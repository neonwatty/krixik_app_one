from decorators.warmer import warmer
from decorators.receiver import receiver_decorator
from receivers.receiver_preprocess.audio_extractor import extract_audio


@warmer
@receiver_decorator(local_input_ext=".mp4", local_output_ext=".mp3")
def lambda_handler(event, context):
    try:
        # extract audio
        extract_audio(event["local_input_path"], event["local_output_path"])

        # return
        message = f"SUCCESS: receiver for {event["receiver_name"]} ran successfully"
        print(message)
        return {"statusCode": 200, "body": {"receiver_name": event["receiver_name"], "message": message}}
    except Exception as e:
        message = f"FAILURE: receiver for {event["receiver_name"]} failed with exception {str(e)}"
        print(message)
        return {"statusCode": 500, "body": {"receiver_name": event["receiver_name"], "message": message}}
