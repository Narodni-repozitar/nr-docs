
from common.services.filtered_record_list import FilteredRecordList
from invenio_rdm_records.services.config import RDMRecordServiceConfig


class FilteredResultServiceConfig(RDMRecordServiceConfig):
    result_list_cls = FilteredRecordList
