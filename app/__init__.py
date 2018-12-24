from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

bootstrap = Bootstrap(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'

from app import routes, models
from app.models import User, Post, Image

if __name__ == "__main__":
    manager.run()
    db.create_all()
