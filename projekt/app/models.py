from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

#ACHTUNG: Dieses modul erwartet, das in der User-Klasse genau 4 Sachen existieren:
# 1: is_authenticated | 2: is_active | 3: is_anonymous | 4: get_id
# --> man muss diese nicht selber schreiben --> das macht man durch UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    aircraft_type = db.Column(db.String(120), nullable=False)
    home_airport = db.Column(db.String(8), nullable=False)


    image_file = db.Column(db.String(20), nullable=False, default='profile.PNG')
    biography = db.Column(db.String(1500))

    image_posts = db.relationship('ImagePost', backref='author', lazy=True, uselist=True)
    route_posts = db.relationship('RoutePost', backref='author', lazy=True, uselist=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class ImagePost(db.Model):
    __tablename__ = 'image_post'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    image = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    number_of_likes = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"ImagePost('{self.image}', '{self.comment}', {self.date_posted})"

class RoutePost(db.Model):
    __tablename__ = 'route_post'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    route = db.Column(db.String(1000), nullable=False)
    number_of_likes = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"RoutePost('{self.route}', '{self.comment}', {self.date_posted})"
