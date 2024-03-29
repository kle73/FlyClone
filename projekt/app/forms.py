from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import User # für die validate_username funktion


#Form zum Registrieren
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    aircraft_type = StringField('What type of aircraft do you fly?', validators=[DataRequired()])
    home_airport = StringField('Your home airport', validators=[DataRequired(), Length(min=3, max=4)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    #raises error if user already exists
    #ACHTUNG kein catch für ValidationErrors notwändig --> nachrichten werden in errors gespeichert
    #ACHTUNG diese Funktionen werden nicht manuell aufgerufen sobald geschrieben --> funktioniert
    def validate_username(self, username):
        #user = None wenn kein user mit dem selben Benutzernamen in der Database gefunden wird
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken please choose a different one!')

    #raises error if email already exists
    def validate_email(self, email):
        #email = None wenn kein user mit der selben Email in der Database gefunden wird
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already taken please choose a different one!')



#Form zum Einloggen
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


#Form zum ändern vom Profil
class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    aircraft_type = StringField('What type of aircraft do you fly?', validators=[DataRequired()])
    home_airport = StringField('Your home airport', validators=[DataRequired(), Length(min=3, max=4)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    picture = FileField('New Profile Picture: ', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken please choose a different one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already taken please choose a different one!')



#Form für das Hochladen von RoutePosts
class PostForm(FlaskForm):
    picture = FileField('Your picture (optional): ', validators=[FileAllowed(['jpg', 'png'])])
    departure = StringField('Departure Airport', validators=[Length(max=4)])
    waypoints = StringField("WayPoints seperated by ';'")
    destination = StringField('Destination Airport', validators=[Length(max=4)])
    departure_date = StringField('When was the departure?', validators=[Length(max=120)])
    landing_date = StringField('When was the landing?', validators=[Length(max=120)])
    plane = StringField('What plane did you fly?', validators=[Length(max=120)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    upload = SubmitField('Post')
