#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:25
# software:PyCharm
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors