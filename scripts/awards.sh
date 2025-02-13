set -e
set -x

invenio oarepo cf init
invenio communities custom-fields init
invenio files location create --default default s3://default;

invenio oarepo fixtures load --verbose

invenio oarepo fixtures load --no-system-fixtures ./fixtures --verbose