import marshmallow as ma
from edtf import Date as EDTFDate
from edtf import Interval as EDTFInterval
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from marshmallow_utils.fields import edtfdatestring as mu_fields_edtf
from nr_metadata.common.services.records.ui_schema import (
    AdditionalTitlesUISchema,
    NRAccessRightsVocabularyUISchema,
    NRAffiliationVocabularyUISchema,
    NRAuthorityRoleVocabularyUISchema,
    NRAuthorityUIUISchema,
    NRContributorUISchema,
    NRCountryVocabularyUISchema,
    NREventUISchema,
    NRExternalLocationUISchema,
    NRFunderVocabularyUISchema,
    NRFundingReferenceUISchema,
    NRGeoLocationPointUISchema,
    NRGeoLocationUISchema,
    NRItemRelationTypeVocabularyUISchema,
    NRLanguageVocabularyUISchema,
    NRLicenseVocabularyUISchema,
    NRLocationUISchema,
    NRRelatedItemUISchema,
    NRResourceTypeVocabularyUISchema,
    NRSeriesUISchema,
    NRSubjectCategoryVocabularyUISchema,
    NRSubjectUISchema,
)
from nr_metadata.documents.services.records.ui_schema import (
    NRDegreeGrantorUISchema,
    NRDocumentMetadataUISchema,
    NRThesisUISchema,
)
from nr_metadata.ui_schema.identifiers import (
    NRAuthorityIdentifierUISchema,
    NRObjectIdentifierUISchema,
    NRSystemIdentifierUISchema,
)
from oarepo_runtime.i18n.ui_schema import (
    I18nStrUIField,
    MultilingualLocalizedUIField,
    MultilingualUIField,
)
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema
from oarepo_runtime.validation import validate_date
from oarepo_vocabularies.services.ui_schemas import HierarchyUISchema, I18nStrUIField


class NrDocumentsUISchema(InvenioUISchema):
    """NrDocumentsUISchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())
    links = ma_fields.Raw()
