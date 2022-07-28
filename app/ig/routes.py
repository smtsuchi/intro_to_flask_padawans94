from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required
from app.ig.forms import CreatePostForm
from app.models import Post, db


ig = Blueprint('ig', __name__, template_folder='igtemplates')


@ig.route('/posts/create', methods=["GET","POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            db.session.add(post)
            db.session.commit()
    return render_template('createpost.html', form=form)

@ig.route('/posts')
def getAllPosts():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)

@ig.route('/posts/delete')
def deletePost():
    return render_template('createpost.html')