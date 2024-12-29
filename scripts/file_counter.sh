#!/bin/bash

# Check if the directory is provided as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Directory to search
directory=$1

# Verify if the provided argument is a valid directory
if [ ! -d "$directory" ]; then
  echo "Error: $directory is not a valid directory"
  exit 1
fi

# Initialize total line count
total_lines=0

# Iterate over all files in the directory recursively
while IFS= read -r -d '' file; do
  # Count the number of lines in the current file
  file_lines=$(wc -l <"$file")
  # Add to total line count
  total_lines=$((total_lines + file_lines))
done < <(find "$directory" -type f -print0)

# Print the total line count
echo "Total lines: $total_lines"
