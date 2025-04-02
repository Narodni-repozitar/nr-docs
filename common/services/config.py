from invenio_rdm_records.services.config import RDMRecordServiceConfig

from common.services.filtered_record_list import FilteredRecordList


class FilteredResultServiceConfig(RDMRecordServiceConfig):

    result_list_cls = FilteredRecordList
    components = []
