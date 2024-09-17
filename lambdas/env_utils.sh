#!/bin/bash

# Function to remove an existing .env file and copy a new one
manage_env_file() {
  local local_env_file="$1"
  local source_env_file="$2"

  # Remove the local .env file if it exists
  if [ -f "$local_env_file" ]; then
    rm "$local_env_file"
    if [ $? -ne 0 ]; then
      echo "Error: Failed to remove existing .env file."
      return 1
    fi
    echo "Existing .env file removed."
  fi

  # Copy the .env file from the source path
  cp "$source_env_file" "$local_env_file"
  if [ $? -ne 0 ]; then
    echo "Error: Failed to copy .env file."
    return 1
  fi

  echo ".env file copied successfully."
}
