#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/10/25 1:06
# software:PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, Required
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    summary = PageDownField('概要', validators=[DataRequired()])
    body = PageDownField('内容', validators=[DataRequired()])
    category = StringField('分类', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    summary = PageDownField('概要', validators=[DataRequired()])
    body = PageDownField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')