#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:22
# software:PyCharm
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
import datetime
from markdown import markdown
import bleach

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def add_role():
        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('密码不可读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    summary = db.Column(db.Text)
    summary_html = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                        'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                tags=allowed_tags, strip=True))

    @staticmethod
    def on_change_summary(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                        'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                tags=allowed_tags, strip=True))


db.event.listen(Post.body, 'set', Post.on_change_body)
db.event.listen(Post.summary, 'set', Post.on_change_summary)

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))

    posts = db.relationship('Post', backref='category', lazy='dynamic')

    @staticmethod
    def count():
        '''
        :return 返回所有分类对象和文章数组成元组的列表，且按文章数降序排列
        '''
        categorys = Category.query.all()
        category_dict = {}
        for i in categorys:
            category_dict[i] = i.posts.count()
        return sorted(category_dict.items(), key=lambda x: x[1], reverse=True)

class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)