#!/bin/bash

#
# Converts a file with NUSL IDs and dates when they were imported to NUSL to python file for timestamp update.
#

if [ $# -lt 1 ]; then
    echo "Error: No input file provided"
    echo "Usage: $0 input_file.csv [output_file.py] [output_directory]"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File $1 does not exist"
    exit 1
fi

output_filename="${2:-identifier_dates.py}"
output_dir="${3:-.}"

if [ ! -d "$output_dir" ]; then
    echo "Error: Directory $output_dir does not exist"
    exit 1
fi

output_file="$output_dir/$output_filename"

if [ -f "$output_file" ]; then
    echo "Removing existing $output_file"
    rm "$output_file"
fi

echo "identifier_dates = {" > "$output_file"

tail -n +1 "$1" | while IFS=',' read -r id date; do
    id=$(echo $id | tr -d '"' | tr -d ' ')
    date=$(echo $date | tr -d '"' | tr -d ' ')

    # Convert the date to ISO format with timezone
    # This will set the time to start of the day (00:00:00) in UTC
    formatted_date="${date}T00:00:00+00:00"
    echo " '$id': '$formatted_date'," >> "$output_file"
done

echo "}" >> "$output_file"

echo "Python dictionary with created timestamps for each record has been created in $output_file"