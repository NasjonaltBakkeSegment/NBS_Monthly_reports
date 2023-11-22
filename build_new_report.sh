#!/bin/bash

# Get the directory of the currently executing script
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $repo_dir/utils/copy_from_ppi.sh
source $repo_dir/utils/build.sh
source $repo_dir/utils/git_push.sh