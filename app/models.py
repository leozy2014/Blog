#coding:utf-8
from . import db
from flask.ext.login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from . import db
from datetime import datetime
import bleach

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(25),unique = True)
    about_me = db.Column(db.String(128))
    email = db.Column(db.String(128))
    qq = db.Column(db.String(13))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    

    def __repr__(self):
        return "<User %r>" %self.username

    @property
    def password(self):
        raise ValueError('cant be read')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


    @login_manager.user_loader
    def user_load(id):
        return User.query.get(int(id))


    def __init__(self,*args,**kwargs):
        super(User,self).__init__(*args,**kwargs)
        if self.role is None:
            if self.username == 'skkg':
                self.role = Role.query.filter_by(name = 'admin').first()
            else:
                self.role = Role.query.filter_by(name = 'user').first()


    def can(self,permission):
        return permission & self.role.permission == permission

    def is_admin(self):
        return self.can(Permissions.ADMIN)

class Anonymous(AnonymousUserMixin):
    username = 'Anonymous'
    def can(self,permission):
        return False
    def is_admin(self):
        return False

    
login_manager.anonymous_user = Anonymous

class Permissions():
    WRITE = 0x01
    COMMIT = 0x02
    ADMIN = 0xff

class Role(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    permission = db.Column(db.Integer)
    name = db.Column(db.String)
    user = db.relationship('User',backref = 'role',lazy = 'dynamic')
    @staticmethod
    def create_roles():
        roles = {'admin':Permissions.ADMIN,
                 'user':Permissions.WRITE |
                 Permissions.COMMIT}

        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permission = roles[r]
            db.session.add(role)
        db.session.commit()


sss = db.Table('sss',
    db.Column('post_id',db.Integer,db.ForeignKey('posts.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'))
    )       

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20),unique = True)
    
    posts = db.relationship('Post',
                            secondary = sss,
                            backref = db.backref('tags',lazy = 'dynamic'),
                            lazy = 'dynamic'
                            )
    def __repr__(self):
        return "<Tag %r>" %self.name

    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(30))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    time = db.Column(db.DateTime,default = datetime.now)
    click_count = db.Column(db.Integer,default = 0)
    like = db.Column(db.Integer,default = 0)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref='post',lazy='dynamic')
    
    def __repr__(self):
        return "<Post %r>" %self.title

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allow = ['a','abbr','acronym','b','blockquote','code',\
                 'em','i','li','ol','pre','strong','ul','h1','h2',\
                 'h3','p','img']
        allow_atr = {'*': ['class'],
                     'img':['src','alt'],
                     'a':['href','rel']}
        target.body_html = bleach.clean(value,tags = allow,
                                        attributes = allow_atr,
                                        strip = True)
        
db.event.listen(Post.body,'set',Post.on_changed_body)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.String(128))
    time = db.Column(db.DateTime,index=True,default= datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))




