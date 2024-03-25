from oarepo_ui.resources.file_resource import S3RedirectFileResource


class DocumentsFileResource(S3RedirectFileResource):
    """DocumentsFile resource."""

    # here you can for example redefine
    # create_url_rules function to add your own rules


class DocumentsFileDraftResource(S3RedirectFileResource):
    """DocumentsFileDraft resource."""

    # here you can for example redefine
    # create_url_rules function to add your own rules
