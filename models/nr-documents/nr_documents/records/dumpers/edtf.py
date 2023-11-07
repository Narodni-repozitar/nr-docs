from oarepo_runtime.records.dumpers.edtf_interval import EDTFIntervalDumperExt


class NrDocumentsEDTFIntervalDumperExt(EDTFIntervalDumperExt):
    """edtf interval dumper."""

    paths = ["metadata/events/eventDate"]


class NrDocumentsDraftEDTFIntervalDumperExt(EDTFIntervalDumperExt):
    """edtf interval dumper."""

    paths = ["metadata/events/eventDate"]
