#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add nusl-offline --name "Offline NUSL harvester" \
            --url https://s3.cl4.du.cesnet.cz --set global --prefix marcxml \
            --loader 's3{bucket=nr-repo-docs-harvest,harvest_name=nusl-harvest-02}' \
            --transformer marcxml --transformer nusl \
            --writer 'service{service=published_documents}'


invenio oarepo oai harvester run nusl-offline
