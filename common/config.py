from flask_resources import HTTPJSONException, create_error_handler
from oarepo_runtime.datastreams.writers.attachments_service import (
    AttachmentsServiceWriter,
)

from common.oai.readers.s3 import S3Reader
from common.oai.writers.timestamp_update import TimestampUpdateWriter
from common.oai.writers.publish_writer import PublishWriter
from common.oai.writers.ownership_writer import OwnershipWriter

DATASTREAMS_READERS = {"s3": S3Reader}
DATASTREAMS_WRITERS = {
    "attachment": AttachmentsServiceWriter,
    "owner": OwnershipWriter,
    "publish": PublishWriter,
    "timestamp_update": TimestampUpdateWriter,
}
