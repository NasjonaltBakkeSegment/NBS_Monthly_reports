#!/bin/bash

# Get the directory of the currently executing script
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if both the month and year arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: You must provide both the year (4 digits) and month (2 digits) as arguments."
    echo "Usage: ./build_new_report.sh <year> <month>"
    exit 1
fi

# Assign the arguments to variables
year="$1"
month="$2"

# Create or overwrite the report_month.yaml file with the provided year and month
yaml_file="$repo_dir/config/report_month.yaml"
echo "month: $month" > $yaml_file
echo "year: $year" >> $yaml_file

# Source the utility scripts
source $repo_dir/utils/copy_from_ppi.sh
source $repo_dir/utils/update_config.sh $year $month
source $repo_dir/utils/build.sh $year $month
source $repo_dir/utils/git_push.sh