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

# check if APP_NAME_PRIVATE is set 
if [ -z "$APP_NAME_PRIVATE" ]; then
  echo "APP_NAME_PRIVATE is not set in .env"
  exit 1
fi

# check if $SERVICE_NAME dockerfile exists in Dockerfiles dir

# login to ecr
echo 'INFO: logging into ecr'
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

# tag image for push 
echo 'INFO: tagging image'
docker tag $ACCOUNT_ID-$SERVICE_NAME $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/$APP_NAME_PRIVATE-$SERVICE_NAME:$STAGE

# push image
echo 'INFO: pushing image'
docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/$APP_NAME_PRIVATE-$SERVICE_NAME:$STAGE