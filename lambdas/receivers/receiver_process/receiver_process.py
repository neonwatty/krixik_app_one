from decorators.warmer import warmer
from decorators.receiver import receiver_decorator
import krixik
import os
import json

KRIXIK_API_URL = os.environ["KRIXIK_API_URL"]
KRIXIK_API_KEY = os.environ["KRIXIK_API_KEY"]

from krixik import krixik
krixik.init(api_key=KRIXIK_API_KEY, api_url=KRIXIK_API_URL)

# create a pipeline with a single transcribe module
pipeline = krixik.create_pipeline(name="yt_shorts_transcribe_app", module_chain=["transcribe"])


@warmer
@receiver_decorator(local_input_ext=".mp3", local_output_ext=".json")
def lambda_handler(event, context):
    try:
        # delete previous run's result
        list_response = pipeline.list(file_names=["yt_shorts_transcription_app.mp3"])
        list_items = list_response["items"]
        if len(list_items) > 0:
            for item in list_items:
                krixik_file_id = item["file_id"]
                delete_result = pipeline.delete(file_id=krixik_file_id)
                assert delete_result["status_code"] == 200
        
        # process the file with the default model
        output_dir = "/".join(event["local_output_path"].split("/")[:-1])
        print(f"output_dir --> {output_dir}")
        process_output = pipeline.process(
            local_file_path=event["local_input_path"],
            local_save_directory=output_dir,
            expire_time=60 * 30, 
            wait_for_process=True,
            verbose=False,
            file_name="yt_shorts_transcription_app.mp3",
            modules={"transcribe": {"model": "whisper-base"}}
        ) 

        # krixik file id
        krixik_file_id = process_output["file_id"]
        print(f"process output from krixik --> {process_output}")
                
        # load in process output from file - here we only print the transcript, and not the timestamped version, since the output is quite long
        transcript = process_output["process_output"][0]
        print(f"transcript --> {transcript}")
                
        # copy krixik file to default output file path
        krixik_file_output_path = output_dir + "/" + f"{krixik_file_id}.json"
        
        # Load the JSON file
        with open(krixik_file_output_path, 'r') as file:
            data = json.load(file)

        # Extract the first element
        first_element = data[0]

        # Save the first element to the output path
        with open(event["local_output_path"], 'w') as file:
            json.dump(first_element, file, indent=4)

        # delete file on krixik server
        krixik_delete_result = pipeline.delete(file_id=krixik_file_id)
        assert krixik_delete_result["status_code"] == 200

        # return
        message = f"SUCCESS: receiver for {event["receiver_name"]} ran successfully"
        print(message)
        return {"statusCode": 200, "body": {"receiver_name": event["receiver_name"], "message": message}}
    except Exception as e:
        message = f"FAILURE: receiver for {event["receiver_name"]} failed with exception {str(e)}"
        print(message)
        return {"statusCode": 500, "body": {"receiver_name": event["receiver_name"], "message": message}}
