from flask import Blueprint, redirect, abort
from invenio_pidstore.models import PersistentIdentifier

nusl_redirect_blueprint = Blueprint(
    'nusl_redirect',
    __name__,
    url_prefix='/nusl'
)

@nusl_redirect_blueprint.route('/<pid>')
def nusl_redirect(pid):
    """Redirect NUSL PID to the actual record."""
    try:
        nusl_pid = PersistentIdentifier.get(pid_type="nusl", pid_value=pid)
        redirect_target = nusl_pid.get_redirect()
        return redirect(f'/docs/{redirect_target.pid_value}')
    except Exception as e:
        print(f"NUSL redirect failed for {pid}: {e}")
        abort(404)