#!/bin/bash

set -e

tx init

tx add remote \
    --file-filter 'translations/<project_slug>.<resource_slug>/<lang>.<ext>' \
    https://www.transifex.com/inveniosoftware/invenio/dashboard/

rm -rf translations

tx pull -l cs -t

msgcat translations/*/cs.po -o messages.po

rm -rf translations
mkdir -p translations/cs/LC_MESSAGES
cat messages.po | grep -v '#, fuzzy' > translations/cs/LC_MESSAGES/messages.po
rm messages.po

pybabel compile -d translations