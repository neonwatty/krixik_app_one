import os
import shutil


def replace_directory(path: str) -> None:
    # Remove the directory if it exists
    if os.path.exists(path):
        shutil.rmtree(path)

    # Create the new directory structure
    os.makedirs(path)


local_input_path = "/tmp/process/input_data"
local_input_file_path = local_input_path + "/" + "input"
local_output_path = "/tmp/process/output_data"
local_output_file_path = local_output_path + "/" + "output"
replace_directory(local_input_path)
replace_directory(local_output_path)
