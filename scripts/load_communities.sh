#!/bin/bash

#
# Loads communities fixtures and its curators.
#

set -e

if [ $# -lt 3 ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 <curator_email> <curator_password> <path_to_fixtures>"
    echo "  curator_email               - Email address for the curator"
    echo "  curator_password            - Password for the curator account"
    echo "  path_to_fixtures            - Path to fixtures directory"
    exit 1
fi

invenio oarepo fixtures load $3 --verbose

invenio users create "$1" --password "$2"

while read -r slug; do
    echo "Processing: Community='$slug' Email='$1'"
    invenio oarepo communities members add "$slug" "$1" curator
done < <(awk '/^slug:/ {print $2}' "$3/communities.yaml" | tr -d '\r')

echo "Processing curators complete"