import datetime
import json
import uuid

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)
