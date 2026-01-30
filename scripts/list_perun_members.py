import sys

from flask import current_app
from flask.cli import with_appcontext
from invenio_app.cli import cli
from oarepo_oidc_einfra.perun import PerunLowLevelAPI


@with_appcontext
def list_perun_members():
    cli = PerunLowLevelAPI(
        current_app.config["EINFRA_API_URL"],
        current_app.config["EINFRA_SERVICE_USERNAME"],
        current_app.config["EINFRA_SERVICE_PASSWORD"],
    )
    all_groups = cli._perun_call(
        "groupsManager",
        "getAllGroups",
        {"vo": current_app.config["EINFRA_REPOSITORY_VO_ID"]},
    )
    for grp in all_groups:
        members = cli._perun_call(
            "groupsManager",
            "getGroupDirectRichMembers",
            {"group": grp["id"]},
        )
        if members:
            print(f'Group {grp["id"]}: {grp["name"]}')
            for member in members:
                print(
                    "   Member:",
                    member["user"]["lastName"],
                    member["user"]["firstName"],
                    member["user"]["id"],
                )


if __name__ == "__main__":
    cli.command("list-perun-members")(list_perun_members)
    sys.argv = ["cli.py", "list-perun-members"]
    cli()
