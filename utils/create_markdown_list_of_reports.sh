#!/bin/bash

# Get the directory of the currently executing script
current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

reports="$current_dir/../reports/"        # Change this to your destination folder path
output_file="$current_dir/../book/previous_reports.md"   # Existing Markdown file name

# Change directory to the destination folder
cd "$reports" || exit

# List all PDF files and create Markdown content
pdf_list=""
shopt -s nullglob
pdf_files=(*.pdf)
if [ ${#pdf_files[@]} -gt 0 ]; then
    for pdf_file in "${pdf_files[@]}"; do
        pdf_list+="* [${pdf_file%.pdf}.pdf](../reports/${pdf_file})"$'\n'
    done
fi

# Write the Markdown content to the output file
{
    echo "# Previous reports"
    echo
    echo "Below is a list of previous reports. If viewing the HTML version of this report online, you can click the link to download a PDF version of a previous report"
    if [ -n "$pdf_list" ]; then
        echo "$pdf_list"
    else
        echo 
        echo "No previous reports available."
    fi
} > "$output_file"

echo "Markdown file '$output_file' created with links to PDF files."