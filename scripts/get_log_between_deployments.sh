#!/bin/bash

# This script is used to get the log between two deployments.
# parameters:
# * $1 - the first deployment tag
# * $2 - the second deployment tag

# Example:
# ./get_log_between_deployments.sh deployment/0.9.1 deployment/0.9.2

set -e

first_deployment_tag=$1
second_deployment_tag=$2

if [ -z "$first_deployment_tag" ] || [ -z "$second_deployment_tag" ]; then
    echo "Please provide the first and second deployment tag"
    exit 1
fi

mkdir -p /tmp/deployment_logs


OUT=/tmp/deployment_logs/log.md

echo "# Log between $first_deployment_tag and $second_deployment_tag" > $OUT
echo "" >> $OUT
echo "## Main repository changes" >> $OUT

git log --oneline $first_deployment_tag..$second_deployment_tag | sed 's/^[^ ]* //' | grep 'Merge' | sed 's/^/- /' >> $OUT
echo "" >> $OUT

# get requirements.txt from the first deployment
git show $first_deployment_tag:requirements.txt | grep 'oarepo-' | sort > /tmp/deployment_logs/first_requirements.txt
git show $second_deployment_tag:requirements.txt  | grep 'oarepo-' | sort > /tmp/deployment_logs/second_requirements.txt


# requirements look like <package>==<version>, iterate and split them
cat /tmp/deployment_logs/first_requirements.txt | while read line; do
    package=$(echo $line | cut -d'=' -f1)
    version=$(echo $line | cut -d'=' -f3)
    echo "First deployment: $package $version"
    # get the version of the package from the second deployment
    second_version=$(grep $package /tmp/deployment_logs/second_requirements.txt | cut -d'=' -f3)
    if [ -z "$second_version" ]; then
        echo "Package $package not found in the second deployment"
    else
        echo "Second deployment: $package $second_version"
        echo "## $package $version -> $second_version" >> $OUT

        package_url="https://api.github.com/repos/oarepo/$package/compare/$version...$second_version"
        echo $package_url
        curl $package_url | jq -r '.commits.[].commit.message' | egrep -v '^[ ]*$' | while read cm ; do
            if echo $cm | grep -q 'Merge'; then
                echo "- *$cm*" >> $OUT
            else
                echo "- $cm" >> $OUT
            fi
        done
        echo "" >> $OUT
    fi
done



