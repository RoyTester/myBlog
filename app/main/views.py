#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/24 23:25
# software:PyCharm
from datetime import datetime
from . import main
from flask import render_template, url_for, redirect, session, flash, request, current_app, jsonify
from .forms import PostForm, EditForm, CommentForm
from .. import db
from ..models import User, Post, Category, Like, Comment
from flask_login import current_user, login_required
import XXProgram as P


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    category_count = Category.count()
    return render_template('index.html', posts=posts, pagination=pagination, category_count=category_count)


@main.route('/about')
def about():
    liked = Like.query.first()
    return render_template('about.html', liked=liked)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            author = 'つ﹏⊂'
        else:
            author = P.faker()[0]
        comment = Comment(body=form.body.data,
                          post=post,
                          author=author)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count()-1)//current_app.config['COMMENTS_PER_PAGE']+1
    pagination = post.comments.order_by(Comment.time.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    return render_template('post.html', post=post, form=form, comments=comments, pagination=pagination)

@main.route('/category/<int:id>')
def category(id):
    page = request.args.get('page', 1, type=int)
    category = Category.query.get_or_404(id)
    pagination = category.posts.order_by(Post.time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('category_search.html', category=category, posts=posts, pagination=pagination)

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = PostForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(tag=form.category.data).first()
        if category is None:
            category = Category(tag=form.category.data)
            db.session.add(category)
            db.session.commit()
        post = Post(title=form.title.data,
                    body=form.body.data,
                    summary=form.summary.data,
                    user=User.query.first(),
                    category=category)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', id=post.id))
    return render_template('write.html', form=form, the_category=Category.query.all())

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = EditForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.summary = form.summary.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.summary.data = post.summary
    return render_template('edit.html', form=form)

@main.route('/like')
def like():
    liked = Like.query.first()
    liked.count += 1
    db.session.add(liked)
    db.session.commit()
    return jsonify({'liked': liked.count})