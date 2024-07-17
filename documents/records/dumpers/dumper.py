from documents.records.dumpers.edtf import (
    DocumentsDraftEDTFIntervalDumperExt,
    DocumentsEDTFIntervalDumperExt,
)
from documents.records.dumpers.multilingual import MultilingualSearchDumperExt
from oarepo_runtime.records.dumpers import SearchDumper
from oarepo_runtime.records.systemfields.mapping import SystemFieldDumperExt


class DocumentsDumper(SearchDumper):
    """DocumentsRecord opensearch dumper."""

    extensions = [
        SystemFieldDumperExt(),
        DocumentsEDTFIntervalDumperExt(),
        MultilingualSearchDumperExt(),
    ]


class DocumentsDraftDumper(SearchDumper):
    """DocumentsDraft opensearch dumper."""

    extensions = [
        SystemFieldDumperExt(),
        DocumentsDraftEDTFIntervalDumperExt(),
        MultilingualSearchDumperExt(),
    ]
