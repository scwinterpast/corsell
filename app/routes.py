from app import app
import os

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy  import SQLAlchemy
from app.models import User, Product, Image, Comment
from app.forms import LoginForm, RegisterForm, UploadForm, CommentForm
from app import db


#HOME PAGE
@app.route('/')
# @login_required #add login view to base.html
def index():
    return render_template('index.html')


#ABOUT US
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in a registered user by adding the user id to the session."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


#REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,\
        firstname=form.firstname.data, lastname=form.lastname.data, \
        contact=form.contact.data, college=form.college.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#PROFILE
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    products = Product.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, products=products)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(APP_ROOT, 'static')
#UPLOAD
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        folder_name = str(current_user.username)
        target = os.path.join(STATIC_ROOT, 'uploads/{}'.format(folder_name))
        if not os.path.isdir(target):
            os.mkdir(target)

        p = Product(title=form.title.data, description=form.description.data,\
        price=form.price.data, author=current_user)
        db.session.add(p)
        db.session.commit()
        print('posted!')

        for f in request.files.getlist('photo'):
            filename = secure_filename(f.filename)
            destination = "/".join([target, filename])
            f.save(destination)

            #For flexibility across differnt computers
            i = destination.find('/static/uploads')
            final_destination = destination[i:]

            product = Product.query.filter_by(author=current_user, title=form.title.data).first()
            i = Image(link=final_destination,user_id=product.id)
            db.session.add(i)
            db.session.commit()

        return redirect(url_for('user', username=current_user.username))

    return render_template('upload.html', form=form)


#PRODUCT
@app.route('/product/<title>/<key>', methods=['GET', 'POST'])
def product(title,key):
    product = Product.query.filter_by(id=key).first()
    comments = Comment.query.filter_by(post_id=product.id).all()
    user = User.query.filter_by(id=product.user_id).first()

    dict = {}
    for c in comments:
        u = User.query.filter_by(id=c.user_id).first()
        if u.username in dict.keys():
            dict[u.username].append(c)
        else:
            dict[u.username]=[c]

    form = CommentForm()
    if form.validate_on_submit():
        c=Comment(text=form.comment.data,post_id=product.id,user_id=current_user.id)
        db.session.add(c)
        db.session.commit()
        comments = Comment.query.filter_by(post_id=product.id).all()
        dict = {}
        for c in comments:
            u = User.query.filter_by(id=c.user_id).first()
            if u.username in dict.keys():
                dict[u.username].append(c)
            else:
                dict[u.username]=[c]
        return render_template('product.html', form=form, product=product, user=user, comments=dict, current=current_user)
    return render_template('product.html', form=form, product=product, user=user, comments=dict, current=current_user)
#     user = User.qery.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(user_id=user.id).all()
#     return render_template('user.html', user=user, posts=posts)
