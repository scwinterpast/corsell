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
from app.models import User, Post, Image
from app.forms import LoginForm, RegisterForm, UploadForm
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
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, posts=posts)


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

        p = Post(title=form.title.data, description=form.description.data,\
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

            post = Post.query.filter_by(author=current_user, title=form.title.data).first()
            i = Image(link=final_destination,user_id=post.id)
            db.session.add(i)
            db.session.commit()

        return redirect(url_for('user', username=current_user.username))

    return render_template('upload.html', form=form)

    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         p = Post()
    #         filename = secure_filename(file.filename)
    #         flash('file {} saved'.format(file.filename))
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('index'))
    # return render_template('upload.html', form=form)
