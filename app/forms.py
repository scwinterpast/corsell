import string
from flask import current_app
from flask_login import current_user

# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField
from wtforms import ValidationError
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo
from app.models import User

class RegisterForm(FlaskForm):
    """Sign Up Form"""
    email = StringField('Email', validators=[DataRequired(), \
    Email(), Length(max=50)])

    username = StringField('Username', validators=[DataRequired(),\
    Length(min=4,max=15)])

    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    contact = StringField('Phone Number', validators=[DataRequired()])
    college = StringField('College', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(),\
    Length(min=8,max=30)])
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[InputRequired('Username is required'),\
    Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired('Password is required'),\
    Length(min=8,max=30)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is None:
    #         raise ValidationError('Username not registered.')
