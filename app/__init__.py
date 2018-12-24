from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'

#UPLOAD
UPLOAD_FOLDER = '/Users/SamuelDNinja/Downloads/corsell/uploads'
# UPLOAD_FOLDER = '/Users/rishabhsarup/Desktop/Corsell/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes, models
