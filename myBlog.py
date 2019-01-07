#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:18
# software:PyCharm
from app import create_app, db
import os
from app.models import User, Role, Post, Category, Like, Comment
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
import click


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post, Category=Category, Like=Like, Comment=Comment)

# command后需要()
@app.cli.command()
def test():
    '''run the test'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.add_role()

    # ensure all users are following themselves
    # User.add_self_follows()