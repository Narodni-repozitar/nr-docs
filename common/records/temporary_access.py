from invenio_rdm_records.records.systemfields import RecordAccessField
from oarepo_runtime.records.systemfields import MappingSystemFieldMixin


class TemporaryRecordAccessField(MappingSystemFieldMixin, RecordAccessField):
    """Temporary record access field."""

    @property
    def mapping(self):
        return {
            "access": {
                "properties": {
                    "record": {
                        "type": "keyword"
                    },
                    "files": {
                        "type": "keyword"
                    },
                    "embargo": {
                        "properties": {
                            "active": {
                                "type": "boolean"
                            },
                            "until": {
                                "type": "date"
                            },
                            "reason": {
                                "type": "text"
                            }
                        }
                    },
                    "status": {
                        "type": "keyword"
                    }
                }
            }
        }
