#
# Import script for 2024-04-08 release
#
# Usage:
# export USER_PASSWORD=<your_password>
# export BUCKET_NAME=<your_bucket_name>
# ./scripts/release_04_08.sh [--destroy] [--harvest]
#
#

cd "$(dirname $0)/.."

set -e
set -x

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --destroy) DESTROY=true ;;
        --harvest) HARVEST=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

export DESTROY
export HARVEST

if [ -d .venv ]; then
    source .venv/bin/activate
fi

if [ -z "$USER_PASSWORD" ] ; then
    echo "USER_PASSWORD is not set"
    exit 1
fi

if [ -z "$BUCKET_NAME" ] ; then
    echo "BUCKET_NAME is not set"
    exit 1
fi

if [ "$DESTROY" == "true" ] ; then
    invenio db destroy --yes-i-know || true
    invenio index destroy --force --yes-i-know || true
    invenio db init create 
    invenio index init
fi

invenio oarepo cf init
invenio communities custom-fields init
invenio files location create --default default s3://${BUCKET_NAME};

invenio oarepo fixtures load --batch-size 1000 --verbose

invenio oarepo fixtures load --no-system-fixtures ./fixtures --batch-size 1000 --verbose

(
cat ./fixtures/communities_v3.4.2.yaml | grep 'slug:' | sed 's/slug: //g' | while read com; do
    cat <<EOF 
- username: nrdocstest+kurator-${com}@gmail.com
  password: ${USER_PASSWORD}
  profile:
    full_name: Kurátor komunity ${com}
  communities:
    - slug: ${com}
      role: curator
- username: nrdocstest+clen-${com}@gmail.com
  password: ${USER_PASSWORD}
  profile:
    full_name: Člen komunity ${com}
  communities:
    - slug: ${com}
      role: member
- username: nrdocstest+prispevatel-${com}@gmail.com
  password: ${USER_PASSWORD}
  profile:
    full_name: Přispěvatel komunity ${com}
  communities:
    - slug: ${com}
      role: submitter
- username: nrdocstest+vlastnik@gmail.com
  password: ${USER_PASSWORD}
  profile:
    full_name: Vlastník - superkurátor
  communities:
    - slug: ${com}
      role: owner
EOF
done 
)>/tmp/nr-docs-users.yaml

invenio documents create-users /tmp/nr-docs-users.yaml

invenio oarepo communities create generic "Obecná komunita"
invenio oarepo communities members add generic "nrdocstest+vlastnik@gmail.com" owner
invenio access allow administration-access user nrdocstest+vlastnik@gmail.com
invenio access allow administration-moderation user nrdocstest+vlastnik@gmail.com

invenio oarepo index reindex
invenio oarepo index reindex

invenio oarepo oai harvester add nusl-manual-submissions --name "Manual submissions NUSL harvester" \
            --url https://invenio.nusl.cz/oai2d --set manual_submission --prefix marcxml \
            --loader 'sickle' \
            --transformer marcxml --transformer nusl \
            --writer 'service{service=documents}' \
            --writer 'attachment{service=documents_file_draft}' \
            --writer 'publish{service=documents}' \
            --writer 'owner{service=documents}' \
            --writer 'timestamp_update{service=documents,date_created_csv_path="./scripts/datecreated.csv"}'

if [ "$HARVEST" == "true" ] ; then
    invenio oarepo oai harvester run nusl-manual-submissions --batch-size 10
fi
