from invenio_access.models import Role


def documents_publish_draft_approver(identity, request_type, topic, creator):
    return Role.query.filter_by(name="curators").first()

def default_receiver(*args, **kwargs):
    return {"group": "curators"}


request_receivers = {
    "documents_publish_draft": documents_publish_draft_approver,
    "documents_edit_record": default_receiver,
    "documents_delete_record": default_receiver,
}
