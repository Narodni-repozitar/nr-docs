import gzip
import os

import boto3
import yaml
from lxml import etree
from oarepo_oaipmh_harvester.readers.sickle import expand_datestamp
from oarepo_runtime.datastreams.readers import BaseReader, StreamEntry
from sickle.models import Record


class S3HarvestReader(BaseReader):
    def __init__(
        self,
        *,
        source=None,
        base_path=None,
        oai_run=None,
        oai_harvester_id=None,
        manual=None,
        bucket=None,
        harvest_name=None,
        **kwargs,
    ):
        super().__init__(source=source, base_path=base_path, **kwargs)
        self.s3_bucket = os.environ.get("NR_DOCS_DUMP_S3_BUCKET", bucket)
        self.s3_prefix = os.environ.get("NR_DOCS_DUMP_S3_HARVEST_NAME", harvest_name)

        self.oai_run = oai_run
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual

    def __iter__(self):
        session = boto3.Session(profile_name="nrdocs-dump")
        s3_client = session.client("s3")

        print(
            f"Initialized s3 client, profile {session.profile_name}, bucket {self.s3_bucket}, prefix {self.s3_prefix}"
        )
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.s3_bucket, Prefix=self.s3_prefix)
        yaml_files = []
        for page in pages:
            for obj in page["Contents"]:
                if obj["Key"].endswith(".yaml.gz"):
                    yaml_files.append(obj["Key"])
        for yaml_file_name in sorted(yaml_files):
            # fetch the yaml file from s3
            zipped_data = s3_client.get_object(
                Bucket=self.s3_bucket, Key=yaml_file_name
            )["Body"]
            unzipped_data = gzip.GzipFile(fileobj=zipped_data, mode="rb")
            content = list(yaml.safe_load_all(unzipped_data))

            for record in content:
                # TODO: handle files section
                parsed_raw = etree.fromstring(record["raw"])
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
