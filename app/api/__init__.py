#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/11/16 17:58
# software:PyCharm
from flask import Blueprint

api = Blueprint('api', __name__)

from . import posts, errors, decorators, authentication