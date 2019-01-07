#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2019/1/6 16:49
# software:PyCharm
from flask import abort
from .models import Permission
from flask_login import current_user
from functools import wraps


def permission_required(perm):
    def decorator(f):
        wraps(f)
        def decoratored_function(*args, **kwargs):
            if not current_user.can(perm):
                abort(403)
            return f(*args, **kwargs)
        return decoratored_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)