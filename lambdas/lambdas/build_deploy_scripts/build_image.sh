#!bin/bash

# Check if at least two arguments are provided
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <service> <arg1> [<arg2> ...]"
  exit 1
fi

# take in command line argument
STAGE=$1
SERVICE_NAME=$2

# Define the local and source .env file paths
RELATIVE_PATH="../../"
DOCKERFILES_DIR="../Dockerfiles"
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

# Check if the Dockerfiles directory exists
if [ ! -d "$DOCKERFILES_DIR" ]; then
  echo "$DOCKERFILES_DIR directory does not exist."
  exit 1
fi

# Check if there is a file or directory named $SERVICE_NAME in the Dockerfiles directory
if [ ! -e "$DOCKERFILES_DIR/$SERVICE_NAME" ]; then
  echo "$SERVICE_NAME does not exist in the Dockerfiles directory."
  exit 1
fi

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found"
  exit 1
fi

# Check if ACCOUNT_ID is set
if [ -z "$ACCOUNT_ID" ]; then
  echo "ACCOUNT_ID is not set in .env"
  exit 1
fi


# build docker image
echo 'INFO: building docker image'
docker buildx build --platform linux/arm64/v8 . --build-context app_root=$RELATIVE_PATH -f ../Dockerfiles/$SERVICE_NAME -t $ACCOUNT_ID-$SERVICE_NAME
