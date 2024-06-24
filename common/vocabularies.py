from oarepo_vocabularies.services.permissions import VocabulariesPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess
from oarepo_runtime.services.config.service import UserWithRole


class NRDocsVocabulariesPermissionPolicy(VocabulariesPermissionPolicy):
    """Permission policy."""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_list_vocabularies = [SystemProcess(), AnyUser()]

    can_create = [SystemProcess(), UserWithRole("curator")]
    can_update = [SystemProcess(), UserWithRole("curator")]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess(), UserWithRole("curator")]
