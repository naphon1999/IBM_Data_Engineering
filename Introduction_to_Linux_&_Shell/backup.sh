#!/bin/bash

# This checks if the number of arguments is correct
# If the number of arguments is incorrect ( $# != 2) print error message and exit
if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit
fi

# This checks if argument 1 and argument 2 are valid directory paths
if [[ ! -d $1 ]] || [[ ! -d $2 ]]
then
  echo "Invalid directory path provided"
  exit
fi

# [TASK 1]
targetDirectory="$1"
destinationDirectory="$2"

# [TASK 2]
echo "Target Directory: $targetDirectory"
echo "Destination Directory: $destinationDirectory"

# [TASK 3]
currentTS=$(date +%s)

# [TASK 4]
backupFileName="backup_${currentTS}.tar.gz"

# We're going to:
  # 1: Go into the target directory
  # 2: Create the backup file
  # 3: Move the backup file to the destination directory

# To make things easier, we will define some useful variables...

# [TASK 5]
origAbsPath=$(pwd)

# [TASK 6]
cd # <-
destDirAbsPath=$(realpath "$destinationDirectory")

# [TASK 7]
cd "$targetDirectory" || { echo "Failed to change directory to $targetDirectory"; exit 1; }
cd "$destinationDirectory" || { echo "Failed to change directory to $destinationDirectory"; exit 1; }

# [TASK 8]
yesterdayTS=$((currentTS - 86400))

declare -a toBackup

for file in $(find . -maxdepth 1) # [TASK 9]
do
  # [TASK 10]
  if ($(stat --format=%Y "$file") -ge "$yesterdayTS")
  then
    # [TASK 11
    toBackup+=("$file")]
  fi
done

# [TASK 12]
backupFileName="backup_$(date +%Y%m%d%H%M%S).tar.gz"
tar -czf "$backupFileName" "${toBackup[@]}"

# [TASK 13]
mv "$backupFileName" "$destAbsPath"

# Congratulations! You completed the final project for this course!
To "upload" your in-progress backup.sh file and continue working on it:
Open a terminal and type touch backup.sh
Open the empty backup.sh file in the editor
Copy-paste the contents of your locally-saved backup.sh file into the empty backup.sh file in the editor
