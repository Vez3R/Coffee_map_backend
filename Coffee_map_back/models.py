from app import db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin , current_user, login_required ,login_user, logout_user


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