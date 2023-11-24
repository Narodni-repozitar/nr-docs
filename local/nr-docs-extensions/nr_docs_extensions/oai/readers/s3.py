import boto3
import datetime
from lxml import etree
from typing import Iterator
import os
import yaml

import pytz
from oarepo_runtime.datastreams import BaseReader, StreamEntry
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch


class SickleReader(BaseReader):
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
        s3_client = boto3.client('s3', endpoint_url=os.environ['NUSL_S3_ENDPOINT_URL'],
                         aws_access_key_id=os.environ['NUSL_S3_ACCESS_KEY'],
                         aws_secret_access_key=os.environ['NUSL_S3_SECRET_KEY'])
        s3_bucket_name = os.environ.get("NUSL_S3_BUCKET", "nr-repo-docs-harvest")
        harvest_name = os.environ.get("NUSL_S3_HARVEST_NAME", 'nusl-harvest-01')

        objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=harvest_name)
        object_keys = [obj['Key'] for obj in objects['Contents'] if obj['Size'] > 0]
        for obj_key in sorted(object_keys):
            _, datestamp, fileno = obj_key.split('/')
            content = list(yaml.safe_load_all(s3_client.get_object(Bucket=s3_bucket_name, Key=obj_key)['Body']))
        
            for record in content:
                header_xml_element = etree.fromstring(record["header"])
                namespaces = { "oai": header_xml_element.nsmap[None] }
                
                status = header_xml_element.xpath("./@status")
                deleted = False if not status else status[0]
                
                identifier = header_xml_element.xpath("//oai:identifier", namespaces=namespaces)                
                if self.identifiers and identifier not in self.identifiers:
                    # skip not requested record
                    continue
                
                datestamp = header_xml_element.xpath("//oai:datestamp", namespaces=namespaces)
                if (self.datestamp_from and self.datestamp_until and self.datestamp_until > datestamp < self.datestamp_from) \
                    or (self.datestamp_from and not self.datestamp_until and datestamp < self.datestamp_from) \
                    or (not self.datestamp_from and self.datestamp_until and self.datestamp_until < datestamp):
                    # skip record out of given time period
                    continue
                setSpecs = header_xml_element.xpath("//oai:setSpec", namespaces=namespaces)
                
                yield StreamEntry(
                    entry=record["raw"],
                    context={
                        "oai": {
                            "metadata": record["metadata"] or {},
                            "datestamp": expand_datestamp(datestamp[0]),
                            "deleted": deleted,
                            "identifier": identifier[0],
                            "setSpecs": setSpecs,
                        },
                        "oai_run": self.oai_run,
                        "oai_harvester_id": self.oai_harvester_id,
                        "manual": self.manual,
                    },
                    deleted=deleted,
                )
        

def expand_datestamp(datestamp):
    if "T" not in datestamp:
        datestamp += "T00:00:00+00:00"
    elif datestamp.endswith("Z") or datestamp.endswith("z"):
        datestamp = datestamp[:-1] + "+00:00"
    elif "+" not in datestamp:
        datestamp += "+00:00"
    return datetime.datetime.fromisoformat(datestamp).astimezone(pytz.utc).isoformat()