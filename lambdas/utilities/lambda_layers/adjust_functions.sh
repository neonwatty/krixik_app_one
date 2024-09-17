#!bin/bash

# take in command line argument
# $1 is the name of the stage
action=$1
stage=$2
config=$3

# Define the local and source .env file paths
RELATIVE_PATH="../../"
LOCAL_ENV_FILE=".env"
ROOT_PATH="../../../"
SOURCE_ENV_FILE="${ROOT_PATH}.env"

# Source the env_utils.sh script and check for failure
source ${RELATIVE_PATH}/env_utils.sh
if [ $? -ne 0 ]; then
  echo "Error: Failed to source env_utils.sh."
  exit 1
fi

# Call the manage_env_file function and check for failure
manage_env_file "$LOCAL_ENV_FILE" "$SOURCE_ENV_FILE"

# deploy config
sls $action -s $stage -c $config



