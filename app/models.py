#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:22
# software:PyCharm
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
import datetime
from markdown import markdown
import bleach
from itsdangerous import Serializer
from flask import current_app, url_for, request
from app.exceptions import ValidationError

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def add_role():
        role = Role.query.filter_by(name='admin').first()
        if role is None:
            role = Role(name='admin')
        role.reset_perm()
        for attr in Permission.__dict__:
            if attr.isupper():
                role.add_perm(getattr(Permission, attr))
        role.default = (role.name == 'user')
        db.session.add(role)
        db.session.commit()

    def has_perm(self, perm):
        return self.permission & perm == perm

    def add_perm(self, perm):
        if not self.has_perm(perm):
            self.permission += perm

    def remove_perm(self, perm):
        if self.has_perm(perm):
            self.permission -= perm

    def reset_perm(self):
        self.permission = 0

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

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        return {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'post_count':self.posts.count()
        }

    def can(self, perm):
        return self.role is not None and self.role.has_perm(perm)
    
    def is_admin(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False
    
    def can(self, perm):
        return False


login_manager.anonymous_user = AnonymousUser


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
                        'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'br', 'img']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                            tags=allowed_tags, strip=True))

    @staticmethod
    def on_change_summary(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                        'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'br', 'img']
        target.summary_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                tags=allowed_tags, strip=True))
    def to_json(self):
        return {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'title': self.title,
            'time': self.time,
            'summary': self.summary,
            'summary_html': self.summary_html,
            # 'user_url': url_for('api.get_user', id=self.user_id),
            # 'category_url': url_for('api.get_category', id=self.category_id),
            # 'comments_url': url_for('api.get_post_comments', id=self.id),
            'comment_count': self.comments.count()
        }

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        title = json_post.get('title')
        summary = json_post.get('summary')
        category_data = json_post.get('category')
        if body == '' or title == '' or summary == '' or category_data == '':
            return ValidationError('message missing')
        category = Category.query.filter_by(tag=category_data).first()
        if category is None:
            category = Category(tag=category_data)
            db.session.add(category)
            db.session.commit()
        return Post(body=body, title=title, summary=summary, category=category)


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

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    disabled = db.Column(db.Boolean)
    author = db.Column(db.Text)
    post = db.relationship('Post', backref=db.backref('comments', lazy='dynamic'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i', 'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        return {
            'url': url_for('api.get_comment', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'time': self.time,
            'post_url': url_for('api.get_post', id=self.post_id),
            'author': self.author,
        }

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comments does not have a body')
        return Comment(body=body)
db.event.listen(Comment.body, 'set', Comment.on_changed_body)