#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:03
# software:PyCharm
from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread

def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MYBLOG_MAIL_SUBJECT-PREFIX']+subject,
                  sender=app.config['MYBLOG_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)
