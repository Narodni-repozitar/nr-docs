#
# Import script for 2024-12-12 release
#
# Usage:
# export USER_PASSWORD=<your_password>
# ./scripts/release_12_02_data.sh [--destroy] [--harvest]
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

invenio oarepo fixtures load --verbose

invenio oarepo fixtures load --no-system-fixtures ./fixtures --verbose

invenio oarepo communities create generic "Obecná komunita"

invenio users create -a -c "nrdocstest+vlastnik@gmail.com" --password "${USER_PASSWORD}" --profile '{"full_name": "Vlastník - superkurátor"}'
invenio oarepo communities members add generic "nrdocstest+vlastnik@gmail.com" owner
invenio access allow administration-access user nrdocstest+vlastnik@gmail.com
invenio access allow administration-moderation user nrdocstest+vlastnik@gmail.com

cat ./fixtures/communities_v3.4.2.yaml | grep 'slug:' | sed 's/slug: //g' | while read com; do
    echo "Creating users for community $com"
    invenio users create -a -c "nrdocstest+kurator-${com}@gmail.com" --password "${USER_PASSWORD}"  --profile "{\"full_name\": \"Kurátor komunity ${com}\"}" &
    invenio users create -a -c "nrdocstest+clen-${com}@gmail.com" --password "${USER_PASSWORD}"  --profile "{\"full_name\": \"Člen komunity ${com}\"}" &
    invenio users create -a -c "nrdocstest+prispevatel-${com}@gmail.com" --password "${USER_PASSWORD}" --profile "{\"full_name\": \"Přispěvatel komunity ${com}\"}" &
    wait
done

cat ./fixtures/communities_v3.4.2.yaml | grep 'slug:' | sed 's/slug: //g' | while read com; do
    echo "Adding users to community $com"
    invenio oarepo communities members add $com "nrdocstest+vlastnik@gmail.com" owner &
    invenio oarepo communities members add $com "nrdocstest+kurator-${com}@gmail.com" curator &
    invenio oarepo communities members add $com "nrdocstest+clen-${com}@gmail.com" &
    invenio oarepo communities members add $com "nrdocstest+prispevatel-${com}@gmail.com" submitter &
    wait
done

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
