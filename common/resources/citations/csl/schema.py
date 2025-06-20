# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CSL based Schema for Invenio RDM Records."""

from edtf import parse_edtf
from edtf.parser.edtf_exceptions import EDTFParseException
from edtf.parser.parser_classes import Date, Interval
from marshmallow import Schema, fields, missing
from marshmallow_utils.fields import SanitizedUnicode


class CSLCreatorSchema(Schema):
    """Creator/contributor common schema."""

    # literal = fields.Method("get_literal")
    given = fields.Str(attribute="person_or_org.given_name", missing=None)
    family = fields.Str(attribute="person_or_org.family_name", missing=None)

    def get_literal(self, obj):
        """Get creator's name."""
        if obj.get("person_or_org", {}).get("name"):
            return obj["person_or_org"]["name"]
        elif obj.get("person_or_org", {}).get("family_name") and obj.get(
            "person_or_org", {}
        ).get("given_name"):
            return f"{obj['person_or_org']['familyName']}, {obj['person_or_org']['givenName']}"
        else:
            return obj.get("role", {}).get("title")


def add_if_not_none(year, month, day):
    """Adds year, month a day to a list if each are not None."""
    _list = []
    _list.append(year) if year else None
    _list.append(month) if month else None
    _list.append(day) if day else None
    return _list


def map_resource_type_to_csl(resource_type):
    mapping = {
        "Annual report": "report",
        "Article": "article-journal",
        "Article - accepted version": "article-journal",
        "Article - corrected version": "article-journal",
        "Article - draft": "article-journal",
        "Article - published version": "article-journal",
        "Article - submitted version": "article-journal",
        "Article - updated version": "article-journal",
        "Book": "book",
        "Book chapter": "chapter",
        "Business trip report": "report",
        "Cartographic material": "map",
        "Certified methodology": "article-journal",
        "Conference paper": "paper-conference",
        "Conference poster": "graphic",
        "Conference presentation": "paper-conference",
        "Conference proceeding": "chapter",
        "Conference programme": "pamphlet",
        "Conservation report": "report",
        "Educational material": "pamphlet",
        "Exhibition catalogue or guide": "pamphlet",
        "Field report": "report",
        "Heritage procedure": "legislation",
        "Methodology without certification": "manuscript",
        "Other": "webpage",
        "Press release": "article-newspaper",
        "Project report": "report",
        "Research report": "report",
        "Review": "review",
        "Specialized map": "map",
        "Statistical or status report": "report",
        "Studies and analyses": "manuscript",
        "Trade literature": "pamphlet",
        "Treatment procedure": "legislation",
    }

    return mapping.get(resource_type, "article-journal")


class CSLJSONSchema(Schema):
    """CSL Marshmallow Schema."""

    id_ = SanitizedUnicode(data_key="id", attribute="id")
    type = fields.Method("get_resource_type")
    title = fields.Method("get_title")
    abstract = fields.Method("get_abstract")
    author = fields.List(
        fields.Nested(CSLCreatorSchema()), attribute="metadata.creators"
    )
    issued = fields.Method("get_issued")
    language = fields.Method("get_language")
    version = SanitizedUnicode(attribute="metadata.version")
    publisher = fields.Method("get_publisher")
    volume = fields.Method("get_volume")
    edition = fields.Method("get_edition")
    issue = SanitizedUnicode(attribute="metadata.series.seriesTitle")
    url = fields.Method("get_url")

    def get_title(self, obj):
        """Get title."""
        sanitized = SanitizedUnicode()._deserialize(
            obj["metadata"].get("title", ""), None, None
        )
        return sanitized

    def get_volume(self, obj):
        metadata = obj["metadata"]
        series = metadata.get("series", [])
        if not series:
            return missing
        return (
            SanitizedUnicode()._deserialize(
                series[0].get("seriesVolume", ""), None, None
            )
            or missing
        )

    def get_edition(self, obj):
        metadata = obj["metadata"]
        series = metadata.get("series", [])
        if not series:
            return missing
        return (
            SanitizedUnicode()._deserialize(
                series[0].get("seriesTitle", ""), None, None
            )
            or missing
        )

    def get_publisher(self, obj):
        """Get publisher."""
        metadata = obj["metadata"]
        sanitized = SanitizedUnicode()._deserialize(
            metadata.get("publishers", [""])[0], None, None
        )
        return sanitized if sanitized else missing

    def get_abstract(self, obj):
        """Get abstract."""
        abstract = obj["metadata"].get("abstract", [])
        return (
            {
                entry["lang"]: {"value": entry["value"]}
                for entry in abstract
                if "lang" in entry and "value" in entry
            }
            if abstract
            else missing
        )

    def get_resource_type(self, obj):
        """Map our resource type to CSL"""
        resource_type = (
            obj["metadata"].get("resourceType", {}).get("title", {}).get("en", "")
        )
        return map_resource_type_to_csl(resource_type)

    def get_issued(self, obj):
        """Get issued dates."""
        try:
            metadata = obj["metadata"]
            date_issued = metadata.get("dateIssued")
            parsed = parse_edtf(date_issued)
        except EDTFParseException:
            return missing
        except StopIteration:
            return missing

        if isinstance(parsed, Date):
            parts = add_if_not_none(parsed.year, parsed.month, parsed.day)
            return {"date-parts": [parts]}
        elif isinstance(parsed, Interval):
            d1 = parsed.lower
            d2 = parsed.upper
            return {
                "date-parts": [
                    add_if_not_none(d1.year, d1.month, d1.day),
                    add_if_not_none(d2.year, d2.month, d2.day),
                ]
            }
        else:
            return missing

    def get_language(self, obj):
        """Get language."""
        metadata = obj["metadata"]
        languages = metadata.get("languages", "")

        if languages:
            language_id = languages[0].get("id")
            return language_id

        return missing

    def get_url(self, obj):
        return obj["links"]["self_html"]
