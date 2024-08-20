
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create documents branch for documents."""



# revision identifiers, used by Alembic.
revision = "documents_1"
down_revision = None
branch_labels = ("documents",)
depends_on = None


def upgrade():
    """Upgrade database."""


def downgrade():
    """Downgrade database."""
