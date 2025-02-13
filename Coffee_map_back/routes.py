from app import appFlask as app, login_manager, db
from models import UsersModel, UserReviewModel, CafeModel
from flask_login import UserMixin, current_user, login_required ,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, make_response

class RoutesClass:
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
        results = []
        for record in records:
            results.append({"name":record.cafe_name,"description":record.description,"image":record.image_link})
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