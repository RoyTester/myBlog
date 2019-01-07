#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/11/16 18:40
# software:PyCharm
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized, forbidden
from app.models import User
from . import api
from flask import g, jsonify
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_token, password):
    if username_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(username_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=username_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('unauthorized')

@api.before_request
@auth.login_required
def before_request():
    if g.current_user.is_anonymous:
        return forbidden('unconfirmed account')

@api.route('/tokens/', methods=['POST'])
def tokens():
    if g.current_user.is_anonymous or g.current_user.token_used:
        return unauthorized('invalid credentials')
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=3600),
        'expiration': 3600
    })
