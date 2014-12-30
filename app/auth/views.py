#coding:utf-8
from . import auth
from flask import render_template,redirect,url_for,flash
from flask.ext.login import login_required, login_user, logout_user
from ..models import User
from .forms import LoginForm,RegForm
from .. import db
from ..decorators import admin_required

@auth.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash(u'成功登陆')
            return redirect(url_for('main.index'))
    return render_template('auth/login.html',form = form)


@auth.route('/reg',methods = ['GET','POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    password = form.password.data,
                    about_me = form.about_me.data,
                    email = form.email.data,
                    qq = form.qq.data,
                    )
        db.session.add(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/reg.html',form = form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@auth.route('/secret')
@admin_required
def secret():
    return 'hahahhahasdfsfsdfsd'
