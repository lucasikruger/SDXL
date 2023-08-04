#!/bin/sh

# Path to the setup.sh script
SETUP_SCRIPT="./setup/setup.sh"
REPO_NAME="stable-diffusion-webui-docker"

# Check if setup.sh exists and is executable
if [ -f "$SETUP_SCRIPT" ] && [ -x "$SETUP_SCRIPT" ]; then
  # Run the setup.sh script
  $SETUP_SCRIPT
  
  cd $REPO_NAME

  # Run the Docker compose command specific to the "auto" profile
  docker compose --profile auto up --build 
  echo "AUTOMATIC1111 profile is up and running."
else
  echo "Error: setup.sh not found or not executable. Please make sure it exists and has execute permissions."
fi
