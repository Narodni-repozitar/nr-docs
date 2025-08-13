from flask import Blueprint, redirect, abort
from invenio_pidstore.models import PersistentIdentifier
from invenio_pidstore.errors import PIDDoesNotExistError

nusl_redirect_blueprint = Blueprint(
    'nusl_redirect',
    __name__,
    url_prefix='/nusl'
)

@nusl_redirect_blueprint.route('/<pid>')
def nusl_redirect(pid):
    try:
        nusl_pid = PersistentIdentifier.get(pid_type="nusl", pid_value=pid)
        redirect_target = nusl_pid.get_redirect()
        
        if redirect_target:
            return redirect(f'/docs/{redirect_target.pid_value}')
    except PIDDoesNotExistError:
        abort(404)