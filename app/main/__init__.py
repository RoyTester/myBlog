#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:25
# software:PyCharm
from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)

@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)

from . import views, errors