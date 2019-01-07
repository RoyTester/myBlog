#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/11/16 18:37
# software:PyCharm
from flask import jsonify, g
from . import api
from .errors import forbidden, unauthorized
from ..models import Post, Permission
from flask import request, url_for, current_app
from .. import db
from .decorators import permission_required


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_posts():
    post = Post.from_json(request.json)
    post.user = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'location': url_for('api.get_post', id=post.id)}


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>/')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())