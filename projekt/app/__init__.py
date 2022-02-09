from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) #static_url_path='/static'
app.config['SECRET_KEY'] = '39487593ujhfsdhsdfssh84'
app.config['WTF_CSRF_SECRET_KEY'] = '39487593hjfgjghj84'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import routes
