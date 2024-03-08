from oarepo_runtime.records.dumpers import SearchDumper
from oarepo_runtime.records.systemfields.mapping import SystemFieldDumperExt

from documents.records.dumpers.edtf import (
    DocumentsDraftEDTFIntervalDumperExt,
    DocumentsEDTFIntervalDumperExt,
)
from documents.records.dumpers.multilingual import MultilingualSearchDumperExt


class DocumentsDumper(SearchDumper):
    """DocumentsRecord opensearch dumper."""

    extensions = [
        SystemFieldDumperExt(),
        DocumentsEDTFIntervalDumperExt(),
        MultilingualSearchDumperExt(),
        DocumentsEDTFIntervalDumperExt(),
    ]


class DocumentsDraftDumper(SearchDumper):
    """DocumentsDraft opensearch dumper."""

    extensions = [
        SystemFieldDumperExt(),
        DocumentsDraftEDTFIntervalDumperExt(),
        MultilingualSearchDumperExt(),
        DocumentsDraftEDTFIntervalDumperExt(),
    ]
