#!/bin/bash

# Check if the source and target directories are provided
if [ $# -ne 2 ]; then
  echo "Usage: $0 <source_directory> <target_directory>"
  exit 1
fi

# Source and target directories
source_dir=$1
target_dir=$2

# Verify if the source directory exists
if [ ! -d "$source_dir" ]; then
  echo "Error: $source_dir is not a valid directory"
  exit 1
fi

# Create the target directory if it does not exist
mkdir -p "$target_dir"

# Initialize a counter for unique filenames
counter=1

# Iterate over all files in the source directory recursively
find "$source_dir" -type f -name "*.jpeg" | while read -r file; do
  # Extract the base filename
  base_name=$(basename "$file")

  # Generate a unique name to avoid duplicates
  unique_name=$(printf "%04d_%s" "$counter" "$base_name")

  # Copy the file to the target directory with the unique name
  cp "$file" "$target_dir/$unique_name"

  # Increment the counter
  counter=$((counter + 1))
done

echo "All files have been copied to $target_dir."
