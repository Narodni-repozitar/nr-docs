import click
import tqdm
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_resources.proxies import current_service_registry

from documents.files.models import DocumentsFileDraftMetadata, DocumentsFileMetadata
from documents.records.models import (
    DocumentsCommunitiesMetadata,
    DocumentsDraftMetadata,
    DocumentsMetadata,
    DocumentsParentMetadata,
    DocumentsParentState,
)


@click.group()
def documents():
    """Documents commands."""


@documents.command()
@click.option("--dry-run", is_flag=True, help="Do not remove documents.")
def remove_all(dry_run):
    """Remove all documents."""

    if not dry_run:
        click.secho(
            """This command will remove all documents !!!
            
It should be used only in development environments and only if you are
absolutely sure what you are doing.
        
Once started, this command can not be stopped. If you are sure 
you want to remove all documents, please type 'YES' in the prompt below.

            """,
            fg="red",
        )

        if input("Are you sure you want to remove all documents? ") != "YES":
            click.secho("Aborted.", fg="red")
            return

    service = current_service_registry.get("documents")
    record_ids = PersistentIdentifier.query.filter_by(pid_type="dcmnts").all()

    for record_id in tqdm.tqdm(record_ids):
        if not dry_run:
            try:
                service.delete(system_identity, record_id.pid_value)
            except:
                try:
                    service.delete_draft(system_identity, record_id.pid_value)
                except:
                    pass
        else:
            click.secho(f"Would remove {record_id.pid_value}", fg="yellow")

    db.session.commit()

    # Remove all files - note: might leave dangling references in the database
    DocumentsFileMetadata.query.delete()
    DocumentsFileDraftMetadata.query.delete()

    # This left traces in the database, remove those
    DocumentsCommunitiesMetadata.query.delete()
    DocumentsParentState.query.delete()
    DocumentsMetadata.query.delete()
    DocumentsDraftMetadata.query.delete()
    DocumentsParentMetadata.query.delete()

    db.session.commit()

    # remove oai records

    click.secho("All documents removed.", fg="green")
