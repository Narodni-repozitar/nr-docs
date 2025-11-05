from flask_principal import ActionNeed
from invenio_access import Permission, superuser_access

no_access = ActionNeed("no-access-for-admin-interface")


class DisabledPermission(Permission):
    """Permission class that denies all access."""

    def __init__(self):
        """Constructor."""
        super().__init__(no_access)
        self.explicit_needs.remove(superuser_access)


def no_admin_access(admin_view):
    """Permission factory that denies all access."""
    return DisabledPermission()
