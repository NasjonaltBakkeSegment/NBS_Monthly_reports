#!/bin/bash

# Get the directory of the currently executing script
current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the directory paths
source_pdf="$current_dir/../book/_build/latex/"
destination="$current_dir/../reports/"
book="$current_dir/../book/"

# Store today's date in a variable
current_date=$(date +"%Y-%m-%d")

# Create the destination directory if it doesn't exist
mkdir -p "$destination"

# Build the PDF report
jb build $book --all --clear-output --builder pdflatex
sleep 5

# Check if the source PDF file exists, then move and rename it
if [ -f "${source_pdf}month.pdf" ]; then
    current_date=$(date +"%Y-%m-%d")
    mv "${source_pdf}month.pdf" "${destination}report_${current_date}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Creating page to list previous reports including links to download PDFs
source $current_dir/create_markdown_list_of_reports.sh

# Building again to include the link to the new PDF report
jb build $book --all --clear-output --builder pdflatex
sleep 5
if [ -f "${source_pdf}month.pdf" ]; then
    current_date=$(date +"%Y-%m-%d")
    mv "${source_pdf}month.pdf" "${destination}report_${current_date}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Build the HTML report
jb build $book --all --clear-output