from oarepo_communities.services.results import RecordCommunitiesComponent
from oarepo_requests.services.results import RequestsComponent, RequestTypesComponent
from oarepo_runtime.services.results import RecordItem, RecordList


class DocumentsRecordItem(RecordItem):
    """DocumentsRecord record item."""

    components = [
        *RecordItem.components,
        RequestsComponent(),
        RequestTypesComponent(),
        RecordCommunitiesComponent(),
    ]


class DocumentsRecordList(RecordList):
    """DocumentsRecord record list."""

    components = [*RecordList.components]
