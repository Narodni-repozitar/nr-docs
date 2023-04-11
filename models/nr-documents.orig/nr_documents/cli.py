import click
import tqdm
import yaml
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_search import current_search
from invenio_search.cli import search_version_check

from nr_documents.proxies import current_service
from nr_documents.records.api import NrDocumentsRecord


@click.group(name="nr-documents")
def group():
    pass


@group.command()
@click.option("--recreate", is_flag=True, help="Drop and create the index")
@click.option("--queue", is_flag=True, help="Use celery to perform bulk indexing")
@with_appcontext
@search_version_check
def reindex(recreate, queue, *args, **kwargs):
    if recreate:
        index = NrDocumentsRecord.index._name
        status = list(current_search.delete(index_list=[index]))
        print_status(f"Delete index {index}: ", status)
        status = list(current_search.create(index_list=[index]))
        print_status(f"Create index {index}: ", status)

    # reindex all
    id_generator = (
        x[0]
        for x in db.session.query(NrDocumentsRecord.model_cls.id).filter(
            NrDocumentsRecord.model_cls.is_deleted.is_(False)
        )
    )

    if queue:
        current_service.indexer.bulk_index(
            # iterator of ids
            id_generator
        )
        print("Records send to the queue")
    else:
        ids = list(id_generator)
        for rec_id in tqdm.tqdm(ids, "Indexing records"):
            record = NrDocumentsRecord.get_record(rec_id)
            current_service.indexer.index(record)
        current_service.indexer.refresh()
        print(f"Indexing finished, indexed {len(ids)} records")


def print_status(title, status):
    print(title)
    for status_val in status:
        for k, v in status_val[1].items():
            print(f"    {k}: {v}")


@group.command()
@click.argument("data-path", type=click.Path(file_okay=True, dir_okay=False))
@with_appcontext
@search_version_check
def load(data_path, *args, **kwargs):
    with open(data_path) as f:
        for doc in tqdm.tqdm(yaml.load_all(f, yaml.SafeLoader), desc="Saving data"):
            current_service.create(system_identity, doc)
