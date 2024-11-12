#!/bin/bash

#
# Imports manually submitted data from NUSL.
#

set -e

# shellcheck disable=SC1090
source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo fixtures load --verbose

invenio oarepo oai harvester add nusl-manual-submissions --name "Manual submissions NUSL harvester" \
            --url https://invenio.nusl.cz/oai2d --set manual_submission --prefix marcxml \
            --loader 'sickle' \
            --transformer marcxml --transformer nusl \
            --writer 'service{service=documents}' \
            --writer 'attachment{service=documents_file_draft}' \
            --writer 'publish{service=documents}' \
            --writer 'owner{service=documents}' \
            --writer 'timestamp_update{service=documents}'

# invenio oarepo oai harvester run nusl-manual-submissions