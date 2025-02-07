from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordDraftsServiceConfig,
)

from common.services.filtered_record_list import FilteredRecordList


class FilteredResultServiceConfig(InvenioRecordDraftsServiceConfig):
    result_list_cls = FilteredRecordList

    components = [
        *InvenioRecordDraftsServiceConfig.components,
    ]
