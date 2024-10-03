#!/bin/bash

# Get the directory of the currently executing script
current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the directory paths
book_dir="$current_dir/../book/"

# Check if both year and month arguments are passed
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: No year or month argument passed to build.sh."
    exit 1
fi

# Assign the arguments to variables
year="$1"
month="$2"

# Define an array of English month names
months=("January" "February" "March" "April" "May" "June" "July" "August" "September" "October" "November" "December")

# Get the month name (subtract 1 from MONTH_INT because arrays are zero-indexed in bash)
month_name=${months[$((month - 1))]}

# Path to your _config.yml file
CONFIG_FILE="${book_dir}_config.yml"

# Use sed to replace the title line with the updated title
sed -i "s/^title:.*/title: NBS monthly report - $year $month_name/" "$CONFIG_FILE"