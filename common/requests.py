from invenio_access.models import Role


def documents_publish_draft_approver(identity, request_type, topic, creator):
    return Role.query.filter_by(name="curators").first()


request_receivers = {
    "documents_publish_draft": documents_publish_draft_approver
}
