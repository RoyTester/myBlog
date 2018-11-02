#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/25 0:35
# software:PyCharm
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

