import copy
import datetime
import gzip
import os
import time
import traceback
from typing import Iterator

import boto3
import pytz
import yaml
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from lxml import etree
from oarepo_runtime.datastreams import BaseReader, StreamEntry
from oarepo_runtime.datastreams.types import StreamEntryFile

load_dotenv()

TWO_WEEKS = 14 * 24 * 3600
BACKOFF_FACTOR = 2
CREATE_PRESIGNED_URL_MAX_ATTEMPTS = 10


def create_presigned_url(s3_client, bucket_name, object_name):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=TWO_WEEKS,
        )
    except ClientError:
        print(traceback.format_exc())
        return None

    return response


class S3Reader(BaseReader):
    def __init__(
        self,
        *,
        all_records=None,
        identifiers=None,
        source=None,
        datestamp_from=None,
        datestamp_until=None,
        oai_run=None,
        oai_harvester_id=None,
        manual=False,
        **kwargs,
    ):
        # we are handling url, so ignore the base path
        super().__init__(source=source, base_path=None, **kwargs)
        self.all_records = all_records
        self.identifiers = identifiers
        self.datestamp_from = datestamp_from
        self.datestamp_until = datestamp_until
        self.oai_run = oai_run
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual

    def __iter__(self) -> Iterator[StreamEntry]:
        s3_client = boto3.client(
            "s3",
            endpoint_url=self.source,
            aws_access_key_id=os.environ["NUSL_S3_ACCESS_KEY"],
            aws_secret_access_key=os.environ["NUSL_S3_SECRET_KEY"],
        )
        s3_bucket_name = os.environ.get("NUSL_S3_BUCKET", "nr-repo-docs-harvest")
        harvest_name = os.environ.get("NUSL_S3_HARVEST_NAME", "nusl-harvest-02")

        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=s3_bucket_name, Prefix=harvest_name)
        size = 0
        for page in pages:
            for obj in page["Contents"]:
                size += obj["Size"]

                yaml_data = s3_client.get_object(Bucket=s3_bucket_name, Key=obj["Key"])[
                    "Body"
                ]
                yaml_data = gzip.GzipFile(fileobj=yaml_data).read().decode("utf-8")
                _, datestamp, _ = obj["Key"].split("/")
                content = list(yaml.safe_load_all(yaml_data))

                for record in content:
                    header_xml_element = etree.fromstring(record["header"])
                    namespaces = {"oai": header_xml_element.nsmap[None]}
                    status = header_xml_element.xpath("./@status")
                    deleted = False if not status else status[0]
                    identifier = header_xml_element.xpath(
                        "//oai:identifier", namespaces=namespaces
                    )

                    not_requested_record = (
                        self.identifiers and identifier not in self.identifiers
                    )
                    if not_requested_record:
                        continue

                    datestamp = header_xml_element.xpath(
                        "//oai:datestamp", namespaces=namespaces
                    )
                    datestamp_is_in_period = (
                        self.datestamp_from
                        and self.datestamp_until
                        and self.datestamp_until > datestamp < self.datestamp_from
                    )
                    datestamp_is_before_period = (
                        self.datestamp_from
                        and not self.datestamp_until
                        and datestamp < self.datestamp_from
                    )
                    datestamp_is_after_period = (
                        not self.datestamp_from
                        and self.datestamp_until
                        and self.datestamp_until < datestamp
                    )
                    record_out_of_period = (
                        datestamp_is_in_period
                        or datestamp_is_before_period
                        or datestamp_is_after_period
                    )
                    if record_out_of_period:
                        continue

                    setSpecs = header_xml_element.xpath(
                        "//oai:setSpec", namespaces=namespaces
                    )

                    record_stream_entries = []
                    for file in record["files"]:
                        backoff_time = 1
                        for _ in range(CREATE_PRESIGNED_URL_MAX_ATTEMPTS):
                            file_presigned_url = create_presigned_url(
                                s3_client, s3_bucket_name, obj["Key"]
                            )

                            if file_presigned_url:
                                break

                            time.sleep(backoff_time)

                            backoff_time *= BACKOFF_FACTOR

                        if not file_presigned_url:
                            print(f"Failed to create the presigned url for {file}.")
                            continue

                        metadata = copy.deepcopy(file)
                        metadata.pop("location")
                        metadata.pop("s3_location")

                        location = file.get("location", None) or file.get(
                            "s3_location", None
                        )

                        metadata["key"] = location.split("/")[-1]

                        record_stream_entries.append(
                            StreamEntryFile(metadata, file_presigned_url)
                        )

                    yield StreamEntry(
                        entry=record["raw"],
                        context={
                            "oai": {
                                "metadata": record["metadata"] or {},
                                "datestamp": expand_datestamp(datestamp[0].text),
                                "deleted": deleted,
                                "identifier": identifier[0].text,
                                "setSpecs": [setSpec.text for setSpec in setSpecs],
                            },
                            "oai_run": self.oai_run,
                            "oai_harvester_id": self.oai_harvester_id,
                            "manual": self.manual,
                        },
                        deleted=deleted,
                        files=record_stream_entries,
                    )


def expand_datestamp(datestamp):
    if "T" not in datestamp:
        datestamp += "T00:00:00+00:00"
    elif datestamp.endswith("Z") or datestamp.endswith("z"):
        datestamp = datestamp[:-1] + "+00:00"
    elif "+" not in datestamp:
        datestamp += "+00:00"
    return datetime.datetime.fromisoformat(datestamp).astimezone(pytz.utc).isoformat()
