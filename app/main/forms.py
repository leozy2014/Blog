#coding:utf-8
from flask.ext.wtf import Form
from wtforms import TextAreaField,SubmitField,StringField,SelectMultipleField
from wtforms.validators import Required,Length
from ..models import Tag

class WriteForm(Form):
    title = StringField(u'标题',validators = [Required(),Length(1,30)])
    body = TextAreaField(u'正文',validators = [Required()])
    tags = StringField(u'标签',validators = [Length(0,60)])
    submit = SubmitField(u'提交')


        
class EditForm(Form):
    title = StringField(u'标题',validators = [Required(),Length(1,30)])
    body = TextAreaField(u'正文',validators = [Required()])
    tags = StringField(u'标签',validators = [Length(0,60)])
    submit = SubmitField(u'提交')

class CommentForm(Form):
    body = StringField(u'Comment',validators = [Required(),Length(1,128)])
    submit = SubmitField(u'提交')
