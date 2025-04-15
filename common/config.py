from oarepo_runtime.datastreams.writers.attachments_service import (
    AttachmentsServiceWriter,
)

from common.oai.readers.s3 import S3Reader
from common.oai.writers.ownership_writer import OwnershipWriter
from common.oai.writers.timestamp_update import TimestampUpdateWriter

DATASTREAMS_READERS = {"s3": S3Reader}
DATASTREAMS_WRITERS = {
    "attachment": AttachmentsServiceWriter,
    "owner": OwnershipWriter,
    "timestamp_update": TimestampUpdateWriter,
}
