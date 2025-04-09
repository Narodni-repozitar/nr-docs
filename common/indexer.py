import os
from flask import current_app
from invenio_search import current_search
from invenio_search.utils import build_index_from_parts

def postprocess(*parts):
    part1 = parts[-1]
    name, version = part1.split("-")
    return (name, *parts[1:-1], part1)

def schema_to_index(schema, index_names=None):
    parts = schema.split("/")

    rec_type, ext = os.path.splitext(parts[-1])
    parts[-1] = rec_type

    if ext not in {
        ".json",
    }:
        return None

    parts = postprocess(*parts)

    if index_names is None:
        index = build_index_from_parts(*parts)
        return index

    for start in range(len(parts)):
        name = build_index_from_parts(*parts[start:])
        if name in index_names:
            return name

    return None

def record_to_index(record):
    """Get index given a record.

    It tries to extract from `record['$schema']` the index.
    If it fails, return the default values.

    :param record: The record object.
    :returns: index.
    """
    # The indices could be defined either in the mappings or in the index_templates
    index_names = list(current_search.mappings.keys()) + list(
        current_search.index_templates.keys()
    )
    schema = record.get("$schema", "")
    if isinstance(schema, dict):
        schema = schema.get("$ref", "")

    index = schema_to_index(schema, index_names=index_names)

    return index or current_app.config["INDEXER_DEFAULT_INDEX"]
