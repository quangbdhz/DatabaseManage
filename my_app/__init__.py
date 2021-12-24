from flask import Flask, request, render_template, app
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:quang810@dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com/ManageUser?charset=utf8mb4"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'

db = SQLAlchemy(app=app)

login_manager = LoginManager(app=app)
login_manager.login_view = "login_account"
login_manager.login_message_category = 'info'

from my_app import routes, admin
from my_app import admin

babel = Babel(app=app)

@babel.localeselector
def get_locale():
    return 'vi'