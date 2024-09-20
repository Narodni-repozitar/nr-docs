#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add nusl-manual-submissions --name "Manual submissions NUSL harvester" \
            --url https://invenio.nusl.cz/oai2d --set manual_submission --prefix marcxml \
            --loader 'sickle' \
            --transformer marcxml --transformer nusl \
            --writer 'service{service=documents}' \
            --writer 'attachment{service=documents_file_draft}' \
            --writer 'publish{service=documents}' \
            --writer 'timestamp_update{service=documents}'

invenio oarepo oai harvester run nusl-manual-submissions