#!/bin/bash

# Get the directory of the currently executing script
current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the directory paths
source_pdf="$current_dir/../book/_build/latex/"
destination="$current_dir/../reports/"
book="$current_dir/../book/"

# Check if both year and month arguments are passed
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: No year or month argument passed to build.sh."
    exit 1
fi

# Assign the arguments to variables
year="$1"
month="$2"

echo "Building report for year: $year and month: $month"

# Create the destination directory if it doesn't exist
mkdir -p "$destination"

# Build the PDF report
jb build $book --all --builder pdflatex
sleep 5

# Check if the source PDF file exists, then move and rename it
if [ -f "${source_pdf}month.pdf" ]; then
    mv "${source_pdf}month.pdf" "${destination}NBS_monthly_report_${year}_${month}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Creating page to list previous reports including links to download PDFs
source $current_dir/create_markdown_list_of_reports.sh

# Building again to include the link to the new PDF report
jb build $book --all --builder pdflatex
sleep 5
if [ -f "${source_pdf}month.pdf" ]; then
    mv "${source_pdf}month.pdf" "${destination}NBS_monthly_report_${year}_${month}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Build the HTML report
jb clean $book
jb build $book --all