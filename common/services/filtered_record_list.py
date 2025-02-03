from invenio_records_resources.services.records.results import RecordList


class FilteredRecordList(RecordList):
    def to_dict(self):
        ret = super().to_dict()
        ret["params"] = {**(self._params or {})}
        return ret
