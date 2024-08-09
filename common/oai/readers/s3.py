import copy
import datetime
import gzip
import logging
import os
import re
import time
import traceback
from io import BytesIO
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

log = logging.getLogger("s3reader")

TWO_WEEKS = 14 * 24 * 3600
BACKOFF_FACTOR = 2
CREATE_PRESIGNED_URL_MAX_ATTEMPTS = 10


class S3Reader(BaseReader):
    """
    Extension of `BaseReader` to process records from S3 service.
    """

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
            aws_access_key_id="IZ20KLUR2O6Q1L1NESIS",
            aws_secret_access_key="deVFi1gcvxT1cd6VXwIG14mV41REIO3dLxgZHqlj",
        )
        s3_bucket_name = os.environ.get("NUSL_S3_BUCKET", "nr-repo-docs-harvest")
        harvest_name = os.environ.get("NUSL_S3_HARVEST_NAME", "nusl-harvest-03")

        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=s3_bucket_name, Prefix=harvest_name)
        size = 0
        for page in pages:
            for obj in page["Contents"]:
                if re.match(
                    r"^.*harvest-\d{2}/\d{4}-\d{2}-\d{2}-to-\d{4}-\d{2}-\d{2}/data/oai.*",
                    obj["Key"],
                ):
                    continue

                size += obj["Size"]

                for i in range(7):
                    try:
                        yaml_data = s3_client.get_object(
                            Bucket=s3_bucket_name, Key=obj["Key"]
                        )["Body"]
                        yaml_data = yaml_data.read()
                        break
                    except:
                        time.sleep(2**i)
                else:
                    raise Exception(f"Failed to download the file {obj['Key']} from S3")

                yaml_data = (
                    gzip.GzipFile(fileobj=BytesIO(yaml_data)).read().decode("utf-8")
                )

                _, datestamp, _ = obj["Key"].split("/")
                content = list(yaml.safe_load_all(yaml_data))

                for record in content:
                    header_xml_element = etree.fromstring(record["header"])
                    namespaces = {"oai": header_xml_element.nsmap[None]}
                    status = header_xml_element.xpath("./@status")
                    deleted = False if not status else status[0]
                    set_specs = header_xml_element.xpath(
                        "//oai:setSpec", namespaces=namespaces
                    )

                    identifier = get_identifier_from_record(
                        header_xml_element, namespaces, record["id"], self.identifiers
                    )
                    if not identifier:
                        continue

                    datestamp = get_valid_datestamp(
                        header_xml_element, namespaces, record["id"]
                    )
                    if datestamp is None or is_record_out_of_period(
                        self.datestamp_until, self.datestamp_from, datestamp
                    ):
                        continue

                    record_stream_entries = []
                    if record["files"]:
                        record_stream_entries = create_stream_entries_from_files(
                            record["files"],
                            s3_client,
                            s3_bucket_name,
                            obj["Key"],
                            record["id"],
                        )

                    yield StreamEntry(
                        entry=record["raw"],
                        context={
                            "oai": {
                                "metadata": record["metadata"] or {},
                                "datestamp": expand_datestamp(datestamp),
                                "deleted": deleted,
                                "identifier": identifier,
                                "setSpecs": [set_spec.text for set_spec in set_specs],
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


def create_presigned_url(s3_client, bucket_name, object_name):
    """
    Generates a presigned URL for downloading an object from S3.

    Parameters:
    - s3_client: The boto3 S3 client instance used for generating the presigned URL.
    - bucket_name (str): The name of the S3 bucket containing the object.
    - object_name (str): The key of the object within the S3 bucket for which to generate the presigned URL.

    Returns:
    - str or None: The presigned URL as a string if the operation is successful;
                   otherwise, None if an error occurs.
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


def create_stream_entries_from_files(
    files, s3_client, s3_bucket_name, obj_key, record_id
):
    """
    Creates stream entries for a list of files associated with a specific record.

    Parameters:
    - files (list of dicts): A list of dictionaries, each representing a file associated with the record.
      Each dictionary contains metadata about the file, including its location.
    - s3_client: The boto3 S3 client instance used for generating the presigned URLs.
    - s3_bucket_name (str): The name of the S3 bucket containing the files.
    - obj_key (str): The object key pattern used to generate presigned URLs for the files.
    - record_id (str): The identifier of the record these files are associated with, used for logging purposes.

    Returns:
    - list of StreamEntryFile: A list of StreamEntryFile objects, each containing metadata and a presigned URL
      for a file.
    """
    stream_entries = []
    for file in files:
        file_presigned_url = get_presigned_url(s3_client, s3_bucket_name, obj_key)
        if not file_presigned_url:
            log.error(
                "Failed to create the presigned url for record: %s and its file: %s",
                record_id,
                file,
            )
            continue

        metadata = copy.deepcopy(file)
        metadata.pop("location")
        metadata.pop("s3_location")

        location = file.get("location", None) or file.get("s3_location", None)
        metadata["key"] = location.split("/")[-1]

        stream_entries.append(StreamEntryFile(metadata, file_presigned_url))

    return stream_entries


def get_presigned_url(s3_client, s3_bucket_name, obj_key):
    """
    Generates a presigned URL for an S3 object, with retries and exponential backoff.

    Parameters:
    - s3_client: The boto3 S3 client instance to use for generating the presigned URL.
    - s3_bucket_name (str): The name of the S3 bucket containing the object.
    - obj_key (str): The key of the object within the S3 bucket for which the presigned URL is generated.

    Returns:
    - str or None: The presigned URL as a string if successful; otherwise, None if all attempts fail.
    """
    backoff_time = 1
    for _ in range(CREATE_PRESIGNED_URL_MAX_ATTEMPTS):
        file_presigned_url = create_presigned_url(s3_client, s3_bucket_name, obj_key)

        if file_presigned_url:
            return file_presigned_url

        time.sleep(backoff_time)

        backoff_time *= BACKOFF_FACTOR

    return None


def get_identifier_from_record(
    header_xml_element, namespaces, record_id, desired_identifiers
):
    """
    Extracts the identifier from a record's XML header and checks if it matches the desired identifiers.

    Parameters:
    - header_xml_element: An XML element object representing the header of the record.
    - namespaces (dict): A dictionary of XML namespaces required for XPath queries.
    - record_id (str): The ID of the record being processed, used for logging purposes.
    - desired_identifiers (list or None): A list of identifiers that are being specifically requested.
                                          If None, all identifiers are considered desired.

    Returns:
    - str or None: The identifier if it is found and matches the desired identifiers; otherwise, None.
    """
    identifier_elements = header_xml_element.xpath(
        "//oai:identifier", namespaces=namespaces
    )
    if not identifier_elements:
        log.error("Identifier is missing for the record: %s", record_id)
        return None

    identifier = identifier_elements[0].text
    if desired_identifiers and identifier not in desired_identifiers:
        return None

    return identifier


def get_valid_datestamp(header_xml_element, namespaces, record_id):
    """
    Extracts the datestamp from a record's XML header.

    Parameters:
    - header_xml_element: An XML element object representing the header of the record.
    - namespaces (dict): A dictionary of XML namespaces required for XPath queries.
    - record_id (str): The ID of the record being processed, used for logging purposes.

    Returns:
    - str or None: The datestamp as a string if it is found and within the specified period; otherwise, None.
    """
    datestamp_elements = header_xml_element.xpath(
        "//oai:datestamp", namespaces=namespaces
    )
    if not datestamp_elements:
        log.warning("Datestamp is not present for the record: %s", record_id)
        return None

    datestamp = datestamp_elements[0].text
    return datestamp


def is_record_out_of_period(datestamp_until, datestamp_from, datestamp):
    """
    Determines if a given datestamp falls outside a specified period.

    Parameters:
    - datestamp_until (datetime or None): The end date of the period. If None, the period is considered
      to extend indefinitely into the future.
    - datestamp_from (datetime or None): The start date of the period. If None, the period is considered
      to have started in the indefinite past.
    - datestamp (datetime): The datestamp to check.

    Returns:
    - bool: True if `datestamp` falls outside the period defined by `datestamp_from` and `datestamp_until`;
      False otherwise.
    """
    datestamp_is_in_period = (
        datestamp_from
        and datestamp_until
        and datestamp_until > datestamp < datestamp_from
    )
    datestamp_is_before_period = (
        datestamp_from and not datestamp_until and datestamp < datestamp_from
    )
    datestamp_is_after_period = (
        not datestamp_from and datestamp_until and datestamp_until < datestamp
    )

    return (
        datestamp_is_in_period
        or datestamp_is_before_period
        or datestamp_is_after_period
    )
