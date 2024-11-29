


from invenio_rdm_records.services.generators import (

    IfRestricted,

)

from invenio_records_permissions.generators import (
    AnyUser,

    SystemProcess,
)
from invenio_records_permissions.policies.records import RecordPermissionPolicy



class DocumentsPermissionPolicy(RecordPermissionPolicy):
    """documents.records.api.DocumentsRecord permissions.
    Values in this class will be merged with permission presets.
    """

    can_search = []
    can_read = []
    can_create = []
    can_update = []
    can_delete = []
    can_manage = []
    can_preview = []
    can_read_files = []
    can_update_files = []


    ###  only for test purposes!!! ###
    # can_read_draft = [IfRestricted("files", then_=[SystemProcess()], else_=[AnyUser()])]
    ###