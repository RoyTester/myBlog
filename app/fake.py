#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/30 12:26
# software:PyCharm
from faker import Faker
from .import db
from .models import User, Post, Category, Role
from sqlalchemy.exc import IntegrityError
from random import randint


# def category(count=10):
#     fake = Faker()
#     i = 0
#     while i < count:
#         category = Category(
#             tag=fake.name(),
#         )
#         db.session.add(category)
#         try:
#             db.session.commit()
#             i += 1
#         except IntegrityError:
#             db.session.rollback()


def post(count=10):
    fake = Faker()
    for i in range(count):
        u = User.query.first()
        c = Category(tag=fake.name(), count=1)
        p = Post(
            title=fake.text(),
            body=fake.text(),
            summary=fake.text(),
            user=u,
            category=c,
            )
        db.session.add(p)
    try:
        db.session.commit()
    except:
        db.session.rollback()
