import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from theblogger.core.views import core
from theblogger.error_pages.handlers import error_pages

### App setup ###

app = Flask(__name__)
app.register_blueprint(core)
app.register_blueprint(error_pages)

### Database setup ###

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

### Login configs ###

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "users.login"
