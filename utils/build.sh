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

# Wait for a few seconds to allow time for the PDF file to be generated
sleep 5  # Adjust the delay time as needed

# Check if the source PDF file exists, then move and rename it
if [ -f "${source_pdf}book.pdf" ]; then
    current_date=$(date +"%Y-%m-%d")
    mv "${source_pdf}book.pdf" "${destination}book_${current_date}.pdf"
else
    echo "The source PDF file does not exist."
fi

# Build the HTML report
jb build ../book/