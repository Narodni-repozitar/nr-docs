#
# Import script for 2024-12-02 release
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

if [ "$DESTROY" == "true" ] ; then
    invenio db destroy --yes-i-know || true
    invenio index destroy --force --yes-i-know || true
    invenio db init create 
    invenio index init
fi

invenio oarepo cf init
invenio communities custom-fields init
invenio files location create --default default s3://default;

invenio oarepo fixtures load --verbose

invenio oarepo fixtures load --no-system-fixtures ./fixtures --verbose

invenio oarepo communities create generic "Obecná komunita"

invenio users create -a -c "vlastnik@test.com" --password "${USER_PASSWORD}" --profile '{"full_name": "Vlastník - superkurátor"}'
invenio oarepo communities members add generic "vlastnik@test.com" owner


cat ./fixtures/communities.yaml | grep 'slug:' | sed 's/slug: //g' | while read com; do
    echo "Creating users for community $com"
    invenio users create -a -c "kurator-${com}@test.com" --password "${USER_PASSWORD}"  --profile "{\"full_name\": \"Kurátor komunity ${com}\"}" &
    invenio users create -a -c "clen-${com}@test.com" --password "${USER_PASSWORD}"  --profile "{\"full_name\": \"Člen komunity ${com}\"}" &
    invenio users create -a -c "prispevatel-${com}@test.com" --password "${USER_PASSWORD}" --profile "{\"full_name\": \"Kurátor komunity ${com}\"}" &
    wait
done

cat ./fixtures/communities.yaml | grep 'slug:' | sed 's/slug: //g' | while read com; do
    echo "Adding users to community $com"
    invenio oarepo communities members add $com "vlastnik@test.com" owner &
    invenio oarepo communities members add $com "kurator-${com}@test.com" curator &
    invenio oarepo communities members add $com "clen-${com}@test.com" &
    invenio oarepo communities members add $com "prispevatel-${com}@test.com" submitter &
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
            --writer 'timestamp_update{service=documents}'

if [ "$HARVEST" == "true" ] ; then
    invenio oarepo oai harvester run nusl-manual-submissions --batch-size 10
fi
