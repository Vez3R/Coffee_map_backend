import uuid
import os

from flask import Flask, render_template, request, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin , current_user, login_required ,login_user, logout_user

db_url = os.getenv("DB_URL", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_login = os.getenv("DB_LOGIN", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_login}:{db_password}@{db_url}:{db_port}/postgres"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class UsersModel(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    login = db.Column(db.Text())
    password = db.Column(db.Text())
    name = db.Column(db.Text())
    
    def set_password(self, password):
	    self.password = generate_password_hash(password)
    
    def check_password(self,  password):
        return check_password_hash(self.password, password)

    def __init__(self, login, name):
        self.login = login
        self.name = name
    
        
class UserReviewModel(db.Model):
    __tablename__ = 'user_review'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True))
    cafe_id = db.Column(db.UUID(as_uuid=True))
    comment = db.Column(db.Text())
    rate = db.Column(db.Integer())

    def __init__(self, user_id, cafe_id, comment, rate):
        self.user_id = user_id
        self.cafe_id = cafe_id
        self.comment = comment
        self.rate = rate
        

class CafeModel(db.Model):
    __tablename__ = 'cafe'

    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    description = db.Column(db.Text())
    metro = db.Column(db.Text())
    image_link = db.Column(db.Text())
    rate = db.Column(db.Float())
    cafe_name = db.Column(db.Text())

    def __init__(self, metro, description, cafe_name, rate, image_link):
        self.metro = metro
        self.cafe_name = cafe_name
        self.rate = rate
        self.description = description
        self.image_link = image_link


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UsersModel).get(user_id)

@app.route('/', methods=['GET'])
def start():
    records = UsersModel.query.all()
    results = [
        {
            "id": record.id,
            "login": record.login,
            "password": record.password
        } for record in records]

    return results

@app.route('/cafe', methods=['GET'])
def get_cafe():
    records = CafeModel.query.all()
    results = {
            "count":len(records),
            "result":[]
            }
    for record in records:
        results["result"].append({"name":record.cafe_name,"metro":record.metro,"description":record.description,"rate":record.rate,"image":record.image_link})
    return results
    
@app.route('/registration', methods=['POST'])
def registration():
    try:
        data = request.get_json()
        new_record = UsersModel(login=data['login'],name=data['name'])
        new_record.set_password(data['password'])
        db.session.add(new_record)
        db.session.commit()
        return {"status": True,"message": "Новая запись успешно добавлена"}
    except Exception as err: 
        print(type(err).__name__)
        return make_response("<h2>Такой логин уже есть</h2>", 404)
    
@app.route('/session', methods=['GET'])
def is_aunt():
    result = {"session":current_user.is_authenticated}
    return result

@app.route('/login', methods=['GET'])
def login():
        user = db.session.query(UsersModel).filter(UsersModel.login == request.args.get('login')).first()
        if user and user.check_password(request.args.get('password')):
            return {"status":login_user(user,remember=True),"message":"Вход успешен"}
        else:
            return make_response("<h2>Введен неверный логин или пароль</h2>", 400)
    
    
@app.route('/logout')
def logout():
    logout_user()
    return {"session":False}  

if __name__=="__main__":
    app.run(port=8080,debug=True)