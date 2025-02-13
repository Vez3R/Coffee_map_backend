import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db_url = os.getenv("DB_URL", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_login = os.getenv("DB_LOGIN", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
appFlask = Flask(__name__)
appFlask.debug = True
appFlask.config['SECRET_KEY'] = 'long secret key'
appFlask.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_login}:{db_password}@{db_url}:{db_port}/postgres"
db = SQLAlchemy(appFlask)
login_manager = LoginManager(appFlask)

from routes import RoutesClass

md = RoutesClass()