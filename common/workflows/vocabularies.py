from invenio_administration.generators import Administration
from oarepo_vocabularies.services.permissions import VocabulariesPermissionPolicy


class DocsVocabulariesPermissionPolicy(VocabulariesPermissionPolicy):
    can_create = VocabulariesPermissionPolicy.can_create + [Administration()]
    can_update = VocabulariesPermissionPolicy.can_update + [Administration()]
    can_edit = VocabulariesPermissionPolicy.can_update + [Administration()]
    can_view_deposit_page = VocabulariesPermissionPolicy.can_create + [Administration()]
