#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/25 17:29
# software:PyCharm
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, errors