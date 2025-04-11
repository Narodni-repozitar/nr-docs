import datetime

import click
import tqdm
import yaml
from celery import current_app as current_celery_app
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_communities.communities.records.api import Community
from invenio_db import db
from invenio_indexer.proxies import current_indexer_registry
from invenio_indexer.tasks import process_bulk_queue
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_resources.proxies import current_service_registry
from werkzeug.local import LocalProxy

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


@documents.command(name="create-users")
@click.argument("file_path")
def create_users(file_path):
    _datastore = LocalProxy(lambda: current_app.extensions["security"].datastore)
    members_service = current_service_registry.get("members")

    with open(file_path, "r") as f:
        user_data = yaml.safe_load(f)
        for user in tqdm.tqdm(user_data):
            username = user["username"]
            password = user.get("password")
            profile = user.get("profile", {})
            communities = user.get("communities", [])

            u = User.query.filter_by(email=username).first()

            if not u:
                from flask_security.utils import hash_password

                # create the user
                u = _datastore.create_user(
                    password=hash_password(password),
                    email=username,
                    active=True,
                    confirmed_at=datetime.datetime.utcnow(),
                    user_profile=profile,
                )
                db.session.add(u)
                db.session.commit()

            user_id = u.id
            for community in communities:
                slug = community["slug"]
                role = community["role"]

                try:
                    community_id = Community.pid.resolve(slug).id
                except:
                    click.secho(f"Community {slug} not found", fg="red")
                    continue

                try:
                    members_service.add(
                        system_identity,
                        community_id,
                        {
                            "members": [
                                {
                                    "type": "user",
                                    "id": str(user_id),
                                }
                            ],
                            "role": role,
                        },
                    )
                except:
                    import traceback

                    traceback.print_exc()
                    click.secho(
                        f"User {username} already in community {slug} or can not be added",
                        fg="red",
                    )
                    continue
        db.session.commit()


@documents.command(name="process-index-queues")
def process_index_queues():
    """Process index queues."""

    channel = current_celery_app.connection().channel()
    indexers = current_indexer_registry.all()

    for name, indexer in indexers.items():
        queue = indexer.mq_queue.bind(channel)
        _, num_messages, num_consumers = queue.queue_declare()
        print(
            f"Indexer {name} has {num_messages} messages and {num_consumers} consumers"
        )
        if num_messages > 0:
            process_bulk_queue.delay(indexer_name=name)
