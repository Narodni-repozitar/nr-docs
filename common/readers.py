import gzip
import os
from sickle.models import Record
from lxml import etree

import yaml

import boto3

from oarepo_runtime.datastreams.readers import BaseReader, StreamEntry
from oarepo_oaipmh_harvester.readers.sickle import expand_datestamp

class S3HarvestReader(BaseReader):
    def __init__(self, *, source=None, base_path=None, oai_run=None, oai_harvester_id=None, manual=None, **kwargs):
        super().__init__(source=source, base_path=base_path, **kwargs)
        self.s3_access_key = os.environ['NR_DOCS_DUMP_S3_ACCESS_KEY']
        self.s3_secret_key = os.environ['NR_DOCS_DUMP_S3_SECRET_KEY']
        self.s3_endpoint_url = os.environ['NR_DOCS_DUMP_S3_ENDPOINT_URL']
        self.s3_bucket = os.environ['NR_DOCS_DUMP_S3_BUCKET']
        self.s3_prefix = os.environ['NR_DOCS_DUMP_S3_HARVEST_NAME']

        self.oai_run = oai_run
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual

    def __iter__(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=self.s3_access_key,
            aws_secret_access_key=self.s3_secret_key,
            endpoint_url=self.s3_endpoint_url
        )
        print(f"Initialized s3 client, endpoint url {self.s3_endpoint_url}, bucket {self.s3_bucket}, prefix {self.s3_prefix}")
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.s3_bucket, Prefix=self.s3_prefix)
        yaml_files = []
        for page in pages:
            for obj in page["Contents"]:
                if obj["Key"].endswith(".yaml.gz"):
                    yaml_files.append(obj["Key"])
        for yaml_file_name in sorted(yaml_files):
            # fetch the yaml file from s3
            zipped_data = s3_client.get_object(Bucket=self.s3_bucket, Key=yaml_file_name)["Body"]
            unzipped_data = gzip.GzipFile(fileobj=zipped_data, mode="rb")
            content = list(
                yaml.safe_load_all(unzipped_data)
            )

            for record in content:
                # TODO: handle files section
                parsed_raw = etree.fromstring(record['raw'])
                record = Record(parsed_raw)

                datestamp = record.header.datestamp
                datestamp = expand_datestamp(datestamp)

                yield StreamEntry(
                    entry=record.raw,
                    context={
                        "oai": {
                            "metadata": record.metadata,
                            "datestamp": datestamp,
                            "deleted": record.header.deleted,
                            "identifier": record.header.identifier,
                            "setSpecs": record.header.setSpecs,
                        },
                        "oai_run": self.oai_run,
                        "oai_harvester_id": self.oai_harvester_id,
                        "manual": self.manual,
                    },
                    deleted=record.header.deleted,
                )


if __name__ == "__main__":
    reader = S3HarvestReader()
    for entry in reader:
        print(entry)

