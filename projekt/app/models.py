from datetime import datetime
from app import app, db, login_manager
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
    destinations = db.Column(db.String(), default=f'{home_airport};')

    image_file = db.Column(db.String(20), nullable=False, default='profile.PNG')
    biography = db.Column(db.String(1500))

    route_posts = db.relationship('Post', backref='author', lazy=True, uselist=True)
    comments = db.relationship('Comment', backref='author', lazy=True, uselist=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"





class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(20))
    description = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    departure = db.Column(db.String(8))
    waypoints = db.Column(db.String(1000))
    destination = db.Column(db.String(8))
    plane = db.Column(db.String(120))
    departure_date = db.Column(db.String(120))
    landing_date = db.Column(db.String(120))
    number_of_likes = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', backref='post', lazy=True, uselist=True)

    def __repr__(self):
        return f"Post('{self.user_id}({self.departure}'| '{self.waypoints}'| {self.destination}))"


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)


with app.app_context():
    db.create_all()


