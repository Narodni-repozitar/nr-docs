from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordDraftsServiceConfig,
)
from nr_docs_extensions.services.filtered_record_list import FilteredRecordList


class FilteredResultServiceConfig(InvenioRecordDraftsServiceConfig):
    result_list_cls = FilteredRecordList