#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/11/16 21:38
# software:PyCharm
from functools import wraps
from flask import g
from .errors import forbidden

def permission_required(permission):
    def decorator(f):
        wraps(f)
        def decorated_func(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('insufficient permission')
            return f(*args, **kwargs)
        return decorated_func
    return decorator
