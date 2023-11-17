#!/bin/bash

# Read YAML content from the file
yaml_file="../config/csv_locations.yaml"
filepaths=$(yq eval '.csv_files | keys | .[]' "$yaml_file")

# Loop through each directory and append filepaths to filenames
while IFS= read -r directory; do
    for file in $(yq eval ".csv_files[\"$directory\"] | .[]" "$yaml_file"); do
        filepath="${directory}${file}"
        scp "$filepath" ../data/
        echo "$filepath"
    done
done <<< "$filepaths"