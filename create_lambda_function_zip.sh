#!/bin/bash

# zip file name
ZIP_FILE_NAME=deployment.zip

# list of files and directories to include in zip file
INCLUDE_FILES=(
  venv/lib/python3.9/site-packages/*
  lambda_function.py
  utils.py
  service_account_key.json
)

# Create a temporary directory
TEMP_DIR=$(mktemp -d)

# Copy files to temporary directory
for file in "${INCLUDE_FILES[@]}"
do
    cp -r "$file" "$TEMP_DIR"
done

# Zip files
cd "$TEMP_DIR" || exit
zip -r9 "$ZIP_FILE_NAME" .

# Move zip file to current directory
mv "$ZIP_FILE_NAME" "$(dirname "$0")"
