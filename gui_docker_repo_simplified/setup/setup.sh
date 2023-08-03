#!/bin/sh

REPO_URL="https://github.com/AbdBarho/stable-diffusion-webui-docker.git"
REPO_NAME="stable-diffusion-webui-docker"

# Navigate one directory back from the setup folder
cd ..

# Check if the directory already exists
if [ -d "$REPO_NAME" ]; then
  echo "The repository $REPO_NAME already exists in the current directory."
else
  # Clone the repository
  git clone $REPO_URL
  echo "The repository $REPO_NAME has been successfully cloned."
fi

# Navigate to the cloned repository folder
cd $REPO_NAME

# Run the Docker compose command to download all required models/files
docker-compose --profile download up --build

echo "Download completed. The models and files are ready for use."
echo "Setup is complete."
