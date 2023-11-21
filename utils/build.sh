#!/bin/bash

# Define the directory paths
source_pdf="../book/_build/pdf/"
destination="../reports/"

# Store today's date in a variable
current_date=$(date +"%Y-%m-%d")

# Create the destination directory if it doesn't exist
mkdir -p "$destination"

# Build the PDF report
jb build ../book/ --builder pdfhtml
sleep 5

# Check if the source PDF file exists, then move and rename it
if [ -f "${source_pdf}book.pdf" ]; then
    current_date=$(date +"%Y-%m-%d")
    mv "${source_pdf}book.pdf" "${destination}book_${current_date}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Creating page to list previous reports including links to download PDFs
source create_markdown_list_of_reports.sh

# Building again to include the link to the new PDF report
jb build ../book/ --builder pdfhtml
sleep 5
if [ -f "${source_pdf}book.pdf" ]; then
    current_date=$(date +"%Y-%m-%d")
    mv "${source_pdf}book.pdf" "${destination}book_${current_date}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Build the HTML report
jb build ../book/