from app import app
import os

import functools
import time
import math
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy  import SQLAlchemy
from app.models import User, Product, Image, Comment
from app.forms import (
    LoginForm, RegisterForm1, RegisterForm2, RegisterForm3, \
    CommentForm, UploadForm1, UploadForm3, FashionForm, LivingForm, PropertyForm, \
    EducationForm, ElectronicsForm, ServicesForm)
from app import db, login

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(APP_ROOT, 'static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'uploads')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


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
    form1 = RegisterForm1()
    form2 = RegisterForm2()
    form3 = RegisterForm3()
    if form1.submit_1.data and form1.validate() and not form2.submit_2.data:
        return render_template('register.html', title='Register', form=form2, step=2);
    if form2.submit_2.data and not form2.validate():
        return render_template('register.html', title='Register', form=form2, step=2);
    if form2.submit_2.data and form2.validate() and not form3.submit_final.data:
        return render_template('register.html', title='Register', form=form3, step=3);
    if form3.submit_final.data and not form3.validate():
        return render_template('register.html', title='Register', form=form3, step=3);
    if form3.submit_final.data and form3.validate():
        user = User(email=form3.email.data, username=form3.username.data, \
        firstname=form3.firstname.data, lastname=form3.lastname.data, \
        contact=form3.contact.data, college=form3.college.data)
        user.set_password(form3.password.data)
        db.session.add(user) #add user to the existing working database
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form= form1, step=1)


#LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#UPLOAD
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form1 = UploadForm1()
    form3 = UploadForm3()
    form2=PropertyForm()
    if form1.category.data == 'property':
        form2=PropertyForm()
    elif form1.category.data == 'fashion':
        form2=FashionForm()
    elif form1.category.data == 'electronics':
        form2=ElectronicsForm()
    elif form1.category.data == 'living':
        form2=LivingForm()
    elif form1.category.data == 'services':
        form2=ServicesForm()
    else:
        form2=EducationForm()

    if form1.submit_1.data and form1.validate() and not form2.submit_2.data:
        print('form1v')
        return render_template('upload.html', title='Upload', form=form2, step=2);
    if form2.submit_2.data and not form2.validate():
        print('form2 fail')
        return render_template('upload.html', title='Upload', form=form2, step=2);
    if form2.submit_2.data and form2.validate() and not form3.submit_final.data:
        print('form 2 ok')
        return render_template('upload.html', title='Upload', form=form3, step=3);
    if form3.submit_final.data and not form3.validate():
        return render_template('upload.html', title='Upload', form=form3, step=3);

    if form3.submit_final.data and form3.validate():
        user_folder = os.path.join(MEDIA_ROOT, str(current_user.username))
        if not os.path.isdir(user_folder):
            os.mkdir(user_folder)
        current_time = math.floor(time.time())
        product_folder = os.path.join(user_folder, str(current_time))
        os.mkdir(product_folder)

        p = Product(title=form3.title.data, description=form3.description.data,\
        price=form3.price.data, author=current_user, timestamp=current_time,\
        condition=form3.condition.data,category=form3.category.data,subcategory=form3.subcategory.data)
        db.session.add(p)
        db.session.commit()

        for f in request.files.getlist('photo'):
            filename = secure_filename(f.filename)
            destination = os.path.join(product_folder, filename)
            f.save(destination)

            link = os.sep + os.path.relpath(destination, APP_ROOT)

            product = Product.query.filter_by(author=current_user, title=form.title.data).first()
            i = Image(link=link ,user_id=product.id)
            db.session.add(i)
            db.session.commit()
    print('here')
    return render_template('upload.html', form=form1, step=1)

#PROFILE
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    products = Product.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, products=products)

#PRODUCT
@app.route('/user/<username>/<key>', methods=['GET', 'POST'])
def product(username,key):
    user = User.query.filter_by(username=username).first_or_404()
    product = Product.query.filter_by(user_id=user.id, timestamp=key).first_or_404()
    comments = Comment.query.filter_by(post_id=product.id).all()
    form=CommentForm()

    d={}
    for comment in comments:
        u=User.query.filter_by(id=comment.user_id).first()
        username=u.username
        if username not in d:
            d[username]=[comment]
        else:
            d[username].insert(0,comment)

    if form.validate_on_submit():
        c=Comment(text=form.comment.data,post_id=product.id,user_id=current_user.id)
        db.session.add(c)
        db.session.commit()

        if current_user.username not in d:
            d[current_user.username]=[c]
        else:
            d[current_user.username].insert(0,c)

        return redirect(url_for('product', username=user.username, key=product.timestamp))

    return render_template('product.html', product=product, user=user, current=current_user, comments=d, form=form)
