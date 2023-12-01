from nr_metadata.services.records.facets.dumper import SyntheticFieldsDumperExtension
from oarepo_runtime.records.dumpers import SearchDumper
from oarepo_runtime.records.systemfields.mapping import SystemFieldDumperExt

from nr_documents.records.dumpers.edtf import (
    NrDocumentsDraftEDTFIntervalDumperExt,
    NrDocumentsEDTFIntervalDumperExt,
)
from nr_documents.records.dumpers.multilingual import MultilingualSearchDumperExt


class NrDocumentsDumper(SearchDumper):
    """NrDocumentsRecord opensearch dumper."""

    extensions = [
        SystemFieldDumperExt(),
        NrDocumentsEDTFIntervalDumperExt(),
        SyntheticFieldsDumperExtension(),
        MultilingualSearchDumperExt(),
    ]


class NrDocumentsDraftDumper(SearchDumper):
    """NrDocumentsDraft opensearch dumper."""

    extensions = [
        SystemFieldDumperExt(),
        NrDocumentsDraftEDTFIntervalDumperExt(),
        SyntheticFieldsDumperExtension(),
        MultilingualSearchDumperExt(),
    ]
