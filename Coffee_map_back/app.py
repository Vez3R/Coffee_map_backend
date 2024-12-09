import datetime
import json
import uuid

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"
db = SQLAlchemy(app)

class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    login = db.Column(db.Text())
    password = db.Column(db.Text())

    def __init__(self, login, password):
        self.login = login
        self.password = password
        
@app.route('/', methods=['GET'])
def start():
    records = UsersModel.query.all()
    results = [
        {
            "login": record.login,
            "password": record.password
        } for record in records]

    return json.dumps(results, default=str)