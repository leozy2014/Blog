#coding:utf-8
from . import main
from flask import render_template,request,abort,redirect,url_for, flash
from ..models import Post,User,Tag,Permissions,Comment
from .forms import WriteForm,EditForm,CommentForm
from ..decorators import permission_required
from flask.ext.login import current_user,login_required
from .. import db



@main.route('/',methods = ['GET','POST'])
def index():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.time.desc()).paginate(page,5)
    posts = pagination.items
    tags = Tag.query.all()
    return render_template('index.html',posts=posts,
                           pagination = pagination,
                           tags = tags,)


@main.route('/page/<id>',methods = ['GET','POST'])
def page(id):
    page = Post.query.get(int(id))
    if page is None:
        abort(404)
    tags = page.tags.all()
    page.click_count = page.click_count+1
    form = CommentForm()
    comments = page.comments.order_by(Comment.time.desc()).all()
    if form.validate_on_submit():
        if not current_user.can(Permissions.COMMIT):
            flash(u'还没登陆啊')
            return redirect(url_for('main.page',id = id))
        comment = Comment(body = form.body.data,
                          post = page,
                          author = current_user._get_current_object()
                          )
        db.session.add(comment)
        return redirect(url_for('main.page',id = id))
    
    return render_template('page.html',page = page ,
                           tags = tags,
                           form = form,
                           comments = comments,
                           )

@main.route('/write',methods = ['GET','POST'])
@permission_required(Permissions.WRITE)
def write():
    form = WriteForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        post = Post(title = form.title.data,
                    body = form.body.data,
                    author = user
                    )
        if form.tags.data != '':
            tag_text = form.tags.data
            tag_text = tag_text.replace(' ','')
            tag_list = [x for x in tag_text.split('#') if x!= '']
            for t in tag_list:
                tag = Tag.query.filter_by(name = t).first()
                if tag is not None:
                    post.tags.append(tag)
                else:
                    tag = Tag(name = t)
                    post.tags.append(tag)
        db.session.add(post)
        return redirect(url_for('main.index') )
    return render_template('write.html',form=form)
    


@main.route('/edit/<id>',methods = ['GET','POST'])
@permission_required(Permissions.WRITE)
def edit(id):
    post = Post.query.get(int(id))
    if  post is None:
        abort(404)
    else:
        form = EditForm()
        if current_user == post.author or current_user.is_admin():
            if form.validate_on_submit():
                post.title = form.title.data
                post.body = form.body.data
                
                old_tags = post.tags.all()
                for tag in old_tags:
                    post.tags.remove(tag)
                    
                if form.tags.data != '':
                    #return form.tags.data
                    tag_text = form.tags.data
                    tag_text = tag_text.replace(' ','')
                    tag_list = [x for x in tag_text.split('#') if x!= '']
                    for t in tag_list:
                        tag = Tag.query.filter_by(name = t).first()
                        if tag is not None:
                            post.tags.append(tag)
                            if tag in old_tags:
                                old_tags.remove(tag)
                        else:
                            tag = Tag(name = t)
                            post.tags.append(tag)
                            
                    for tag in old_tags:
                        if len(tag.posts.all()) == 0:
                            db.session.delete(tag)
                            
                return redirect(url_for('main.page',id = post.id))
            form.title.data = post.title
            form.body.data = post.body
            tag_text = ' # '.join([x.name for x in post.tags.all()])
            form.tags.data = tag_text
        else:
            abort(403)

        return render_template('edit.html',form = form)
                

@main.route('/delete/<id>')
@login_required
def delete(id):
    post = Post.query.get(int(id))
    if post is None:
        abort(404)
    if (current_user._get_current_object() == post.author)or\
       current_user.is_admin():
        tag_list = post.tags.all()
        for tag in tag_list:
            if len(tag.posts.all()) == 1:
                db.session.delete(tag)
        db.session.delete(post)
        return redirect(url_for('main.index'))
    else:
        abort(403)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    else:
        posts = user.posts.all()[0:5]
        return render_template('user.html',user = user,posts = posts)




@main.route('/tag/<tagname>')
def tag(tagname):
    tag = Tag.query.filter_by(name = tagname).first()
    if tag is None:
        abort(404)
    posts = tag.posts.all()
    return render_template('search.html',posts = posts)
    
