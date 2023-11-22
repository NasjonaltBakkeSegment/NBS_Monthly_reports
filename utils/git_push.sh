#!/bin/bash

# Add all changes
git add --all

# Commit changes with a default commit message
git commit -m "Automatic commit and push after building new report"

# Push changes to the 'master' branch on the remote named 'origin'
git push origin master

# Publishing the report with GitHub pages
ghp-import -n -p -f ../book/_build/html