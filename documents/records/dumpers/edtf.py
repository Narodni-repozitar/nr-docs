from oarepo_runtime.records.dumpers.edtf_interval import EDTFIntervalDumperExt


class DocumentsEDTFIntervalDumperExt(EDTFIntervalDumperExt):
    """edtf interval dumper."""

    paths = ["metadata/events/eventDate"]


class DocumentsDraftEDTFIntervalDumperExt(EDTFIntervalDumperExt):
    """edtf interval dumper."""

    paths = ["metadata/events/eventDate"]
