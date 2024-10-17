#!/bin/bash

#
# Resets the repository after harvesting & imports all needed fixtures.
#

set -e

invenio db destroy --yes-i-know || true                                                                                                                                                                                                             ─╯
invenio db init create      
invenio index destroy --force --yes-i-know || true
invenio index init
invenio oarepo cf init
invenio files location create --default default s3://default;
invenio oarepo index reindex
invenio oarepo index reindex