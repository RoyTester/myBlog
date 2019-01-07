#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/11 18:12
# software:PyCharm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail, Message
from config import config
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pagedown import PageDown

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)
# mysql+pymysql为mysql连接uri，非mysql:，非url
    app.config.from_object(config[config_name])
    db.init_app(app)
    mail.init_app(app)
    config[config_name].init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app





