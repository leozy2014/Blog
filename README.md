Blog
====
#简介:

简单的博客,具备基本的博客浏览发布评论及简单的管理功能。数据使用的SQLite
#功能:
 注册登陆
 
 评论
 
 集成了ckeditor富文本
 
 Tag分类
 
可惜没用virtualenv...
#环境:
python2.7.8

bleach

flask

flask-sqlalchemy

flask-login

flask-bootstrap

flask-manager

flask-wtf

werkzeug

#使用方法
先在python manage.py shell里面

from app import db

from app.models import Role

db.create_all()

Role.create_roles()

然后python manage.py runserver


自己注册一个用户名是skkg的就自动是管理员
