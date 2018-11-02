#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/25 17:30
# software:PyCharm
from . import auth
from .forms import LoginForm
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data=='y')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误')
    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    # flash('退出成功')
    return redirect(url_for('main.index'))