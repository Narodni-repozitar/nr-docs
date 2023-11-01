from oarepo_runtime.records.dumpers import SearchDumper

from nr_documents.records.dumpers.edtf import (
    NrDocumentsDraftEDTFIntervalDumperExt,
    NrDocumentsEDTFIntervalDumperExt,
)
from nr_documents.records.dumpers.multilingual import MultilingualSearchDumperExt


class NrDocumentsDumper(SearchDumper):
    """NrDocumentsRecord opensearch dumper."""

    extensions = [NrDocumentsEDTFIntervalDumperExt(), MultilingualSearchDumperExt()]


class NrDocumentsDraftDumper(SearchDumper):
    """NrDocumentsDraft opensearch dumper."""

    extensions = [
        NrDocumentsDraftEDTFIntervalDumperExt(),
        MultilingualSearchDumperExt(),
    ]
