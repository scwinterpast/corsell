from app import db
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class User( UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    contact = db.Column(db.String(15))
    college = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    products = db.relationship('Product', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def avatar(self, size):
    #     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    #         digest, size)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(140))
    price = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('Image', backref='listing', lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.title)

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return '<Image {}>'.format(self.link)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
