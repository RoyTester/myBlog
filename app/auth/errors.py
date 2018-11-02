#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/31 17:04
# software:PyCharm
from . import auth
from flask import render_template

@auth.app_errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400