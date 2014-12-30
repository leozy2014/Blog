from functools import wraps
from flask.ext.login import current_user
from flask import abort
from .models import Permissions

def permission_required(permission):
    def deco(f):
        @wraps(f)
        def deco2(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return deco2
    return deco


def admin_required(f):
    return permission_required(Permissions.ADMIN)(f)
