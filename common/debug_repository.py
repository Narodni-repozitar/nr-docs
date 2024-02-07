from invenio_app.cli import cli

if __name__ == "__main__":
    cli.main(
        # args=[
        #     "run",
        #     "--cert",
        #     "./docker/development.crt",
        #     "--key",
        #     "./docker/development.key",
        # ]
        args=[
            "oarepo",
            "oai",
            "harvester",
            "run",
            "nusl_s3_composite",
        ]
    )
