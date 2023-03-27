#!/bin/bash

set -e

pth=$(readlink -f $(dirname $0))
echo "Source data for installation are in $pth"

if [ a"$NR_DOCS_DIR" == "a" ] ; then
  NR_DOCS_DIR="$pth/../nr-documents"
fi

rsync --progress -a $pth/site/ $NR_DOCS_DIR/sites/nr-docs/
rsync --progress -a $pth/ui/ $NR_DOCS_DIR/ui/docs-app/docs_app/
