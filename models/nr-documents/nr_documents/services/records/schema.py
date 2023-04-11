import marshmallow as ma
from edtf import Date as EDTFDate
from edtf import Interval as EDTFInterval
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from invenio_vocabularies.services.schema import i18n_strings
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from marshmallow_utils.fields import edtfdatestring as mu_fields_edtf
from nr_metadata.common.services.records.schema import (
    AdditionalTitlesSchema,
    NRAccessRightsVocabularySchema,
    NRAffiliationVocabularySchema,
    NRAuthorityRoleVocabularySchema,
    NRAuthoritySchema,
    NRContributorSchema,
    NRCountryVocabularySchema,
    NREventSchema,
    NRExternalLocationSchema,
    NRFunderVocabularySchema,
    NRFundingReferenceSchema,
    NRGeoLocationPointSchema,
    NRGeoLocationSchema,
    NRItemRelationTypeVocabularySchema,
    NRLanguageVocabularySchema,
    NRLicenseVocabularySchema,
    NRLocationSchema,
    NRRelatedItemSchema,
    NRResourceTypeVocabularySchema,
    NRSeriesSchema,
    NRSubjectCategoryVocabularySchema,
    NRSubjectSchema,
)
from nr_metadata.documents.services.records.schema import (
    NRDegreeGrantorSchema,
    NRDocumentMetadataSchema,
    NRThesisSchema,
)
from nr_metadata.schema.identifiers import (
    NRAuthorityIdentifierSchema,
    NRObjectIdentifierSchema,
    NRSystemIdentifierSchema,
)
from oarepo_runtime.i18n.schema import I18nStrField, MultilingualField
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.validation import validate_date, validate_datetime
from oarepo_vocabularies.services.schemas import HierarchySchema


class NrDocumentsSchema(InvenioBaseRecordSchema):
    """NrDocumentsSchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataSchema())
