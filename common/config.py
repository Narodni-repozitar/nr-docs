from common.oai.readers.s3 import S3Reader
from common.oai.writers.composite import CompositeWriter

DATASTREAMS_READERS = { "s3": S3Reader }
DATASTREAMS_WRITERS = { "composite": CompositeWriter }
