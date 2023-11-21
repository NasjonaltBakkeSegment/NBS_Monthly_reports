#!/bin/bash

# Get the directory of the currently executing script
current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read YAML content from the file
yaml_file="$current_dir/../config/csv_locations.yaml"
filepaths=$(yq eval '.csv_files | keys | .[]' "$yaml_file")

# Loop through each directory and append filepaths to filenames
while IFS= read -r directory; do
    for file in $(yq eval ".csv_files[\"$directory\"] | .[]" "$yaml_file"); do
        filepath="${directory}${file}"
        rsync -avz -e ssh "$filepath" "$current_dir"/../data/
        echo "$filepath"
    done
done <<< "$filepaths"