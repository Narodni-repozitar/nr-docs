from oarepo_runtime.resources.responses import ExportableResponseHandler
from oarepo_runtime.i18n import lazy_gettext as _
from .datacite import DataciteSerializer

datacite_serializer = {
    "application/vnd.datacite.datacite+json": ExportableResponseHandler(
        export_code="datacite",
        name=_("Datacite"),
        serializer=DataciteSerializer()
    )
}

