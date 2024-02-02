#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# PLEASE SET THE FOLLOWING VARIABLES IN YOUR .envrc.local
#
# export NR_DOCS_DUMP_S3_ACCESS_KEY=...
# export NR_DOCS_DUMP_S3_SECRET_KEY=...
# export NR_DOCS_DUMP_S3_ENDPOINT_URL=https://s3.cl4.du.cesnet.cz
# export NR_DOCS_DUMP_S3_HARVEST_NAME=nusl-harvest-02
# export NR_DOCS_DUMP_S3_BUCKET=nr-repo-docs-harvest


# shellcheck disable=SC1090
source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add nusl-offline --name "Offline NUSL harvester" \
            --url https://s3.cl4.du.cesnet.cz --set global --prefix marcxml \
            --loader s3 --transformer marcxml --transformer nusl \
            --writer 'service{service=published_documents}'


invenio oarepo oai harvester run nusl-offline --log-level INFO
