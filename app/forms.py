import string
from flask import current_app
from flask_login import current_user

# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField, TextAreaField, SelectField, RadioField, DecimalField
from wtforms import ValidationError
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User

class RegisterForm(FlaskForm):
    """Sign Up Form Template"""
    email = StringField('Email')
    username = StringField('Username')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    contact = StringField('Phone Number')
    college = StringField('College')
    password = PasswordField('Password')
    confirm = PasswordField('Verify password')

class RegisterForm1(RegisterForm):
    """Sign Up Form Part 1"""
    email = StringField('Email', validators=[DataRequired(), \
    Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(),\
    Length(min=8,max=30)])
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')])
    submit_1 = SubmitField('Next')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class RegisterForm2(RegisterForm1):
    """Sign Up Form Part 2"""
    username = StringField('Username', validators=[DataRequired(),\
    Length(min=4,max=15)])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    submit_2 = SubmitField('Next')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
            raise ValidationError('Please use a different email address.')

class RegisterForm3(RegisterForm2):
    """Sign Up Form Part 3"""
    contact = StringField('Phone Number', validators=[DataRequired()])
    college = StringField('College', validators=[DataRequired()])
    submit_final = SubmitField('Register')

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(message='Username is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    """Upload Form"""
    title = StringField('Title', validators=[DataRequired(message='Title is required')])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    price = DecimalField('Price', validators=[DataRequired(message='Price is required'),\
    NumberRange(min=0, message='Price must be a valid number, at least 0')])
    photo = FileField('Image', validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'], 'Images only!')])
    condition = SelectField(u'Condition', choices=[('na','N/A'),('new','New'),('used','Used')])
    category = SelectField(u'Category', validators=[DataRequired(message='Category is required')],\
    choices=[('property','Cars & Housing'),('fashion','Fashion'),('living','Living'),\
    ('education','Education'),('services','Serivces'),('electronics','Electronics')])
    # subcategory = SelectField()
    submit_1 = SubmitField('Next')
    submit_2 = SubmitField('Next')
    submit_final = SubmitField('Upload')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is None:
    #         raise ValidationError('Username not registered.')
    #     if user is not None and
    #
    # def validate_password(self, username, password):
    #     user = User.query.filter_by(username=username.data).first()
    #     if not user.check_password(password.data):
    #         raise ValidationError('Incorrect password.')

class CommentForm(FlaskForm):
    """Comment Form"""
    comment = TextAreaField('Post a comment:',validators=[DataRequired()])
    submit = SubmitField("Post")

class UploadForm(FlaskForm):
    """Upload Form Template"""
    title = StringField('Title')
    description = TextAreaField('Description')
    price = DecimalField('Price')
    photo = FileField('Image')
    condition = SelectField(u'Condition')
    category = SelectField(u'Category')
    subcategory = SelectField(u'Subcategory')

class UploadForm1(UploadForm):
    """Upload Form Part 1"""
    photo = FileField('Image', validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'], 'Images only!')])
    submit_1 = SubmitField('Next')

class UploadForm2(UploadForm1):
    """Upload Form Part 2"""
    title = StringField('Title', validators=[DataRequired(message='Title is required')])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    price = DecimalField('Price', validators=[DataRequired(message='Price is required'),\
    NumberRange(min=0, message='Price must be a valid number, at least 0')])
    condition = SelectField(u'Condition', choices=[('na','N/A'),('new','New'),('used','Used')])
    category = SelectField(u'Category', validators=[DataRequired(message='Category is required')],\
    choices=[('property','Cars & Housing'),('fashion','Fashion'),('living','Living'),\
    ('education','Education'),('services','Services'),('electronics','Electronics')])
    submit_2 = SubmitField('Next')

class PropertyForm(UploadForm2):
    """Upload Form Part 3 - Cars & Housing"""
    subcategory = SelectField(u'Subcategory', choices=[('cars','Cars'),('sublet','Subletting'),('lease','Leasing')])
    submit_final = SubmitField('Upload')

class FashionForm(UploadForm2):
    """Upload Form Part 3 - Fashion"""
    subcategory = SelectField(u'Subcategory', choices=[('watches','Watches'),('accessories','Accessories'),\
    ('bags','Bags'),('wallets','Wallets'),('jackets','Jackets & Sweaters'),('tops','Tops'),\
    ('bottoms','Bottoms'),('footwear','Footwear'),('jewellery','Jewellery'),\
    ('health&beauty','Health & Beauty')])
    submit_final = SubmitField('Upload')

class LivingForm(UploadForm2):
    """Upload Form Part 3 - Living"""
    subcategory = SelectField(u'Subcategory', choices=[('furniture','Furniture'),\
    ('bedsandmattresses','Beds & Mattresses'),('shelvesanddrawers','Shelves & Drawers'),\
    ('sofas','Sofas'),('tablesandchairs','Tables & Chairs'),('decor','Home Decor'),\
    ('plants','Plants'),('gardening','Gardening Tools'),('tv','TVs & Entertainment Systems'),\
    ('kitchen','Kitchenware'),('laundry','Cleaning & Laundry'),('aircare','Cooling & Air Care')])
    submit_final = SubmitField('Upload')

class EducationForm(UploadForm2):
    """Upload Form Part 3 - Education"""
    subcategory = SelectField(u'Subcategory', choices=[('textbooks','Textbooks'),\
    ('iclickers','Iclickers'),('stationery','Stationery'),('calculators','Calculators')])
    submit_final = SubmitField('Upload')

class ElectronicsForm(UploadForm2):
    """Upload Form Part 3 - Electronics"""
    subcategory = SelectField(u'Subcategory', choices=[('audio','Audio'),\
    ('computers','Computers'),('computerparts','Computer Parts & Accessories'),\
    ('phones','Mobile Phones'),('tablets','Tablets'),('mobileparts','Mobile & Tablet Accessories')])
    submit_final = SubmitField('Upload')

class ServicesForm(UploadForm2):
    """Upload Form Part 3 - Services"""
    subcategory = SelectField(u'Subcategory', choices=[('photography','Photography'),\
    ('haircuts','Haircuts'),('tuition','Tuition'),('flowers','Flowers & Bouquets'),\
    ('repairs','Home Repairs'),('rides','Ride Hitching')])
    submit_final = SubmitField('Upload')
