#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField,BooleanField,TextAreaField
from wtforms.validators import Required,EqualTo,Length
from ..models import User


class LoginForm(Form):
    username = StringField(u'用户名',validators = [Required()])
    password = PasswordField(u'密码',validators = [Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegForm(Form):
    username = StringField(u'用户名',validators = [Required()])
    password = PasswordField(u'密码',validators = [Required()])
    password2 = PasswordField(u'请再输入密码',validators = [Required(),EqualTo('password',u'两次输入的密码不一样')])
    about_me = TextAreaField(u'关于我?',validators = [Length(0,128)])
    email = StringField(u'E-mail',validators = [Length(0,58)])
    qq = StringField(u'QQ',validators = [Length(0,13)])
    submit = SubmitField(u'注册')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValueError('the username is already in use')
