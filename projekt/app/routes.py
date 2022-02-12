import os
import itertools
import secrets
from PIL import Image
from flask import render_template, request, url_for, flash, redirect
from app import app, db, bcrypt #from app --> immer nur __init__ durchsucht
from app.forms import RegistrationForm, LoginForm, EditProfileForm, PostForm
from app.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required




###############################################################################
#########################Register and Login views##############################
###############################################################################


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        #sucht user, von dem der username übereinstimmt wenn es keinen gibt --> None
        user = User.query.filter_by(username=form.username.data).first()
        #user soll nicht None sein und passwörter müssen übereinstimmen
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #logged user automatisch ein (Wenn remember gibt --> hier als 2. Parameter einfügen)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful: Please check username or password.')

    return render_template('login.html', form=form)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        #creating a new user und store it in db:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password, name=form.name.data,
                    aircraft_type=form.aircraft_type.data,
                    home_airport=form.home_airport.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created you can now Log in!', 'succsess')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





###############################################################################
############################ Home Views #######################################
###############################################################################

###########METHODS##############

# returns a variable that makes sure the profile page gets formated correctly, based on the profile-picture-size
def get_picture_x(pic):
    img = Image.open(pic)
    width, height = img.size
    new_width = width // (height//80)
    return (new_width - 100)

def save_profile_picture(form_picture):
    random_name = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename) #--> funktion gibt zwei werte zurück: 1. name und 2. extention (z.B. .jpg) der _ sorgt dafür, dass wir den namen 'wegschmeißen'
    picture_filename = random_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_filename)
    form_picture.save(picture_path)
    return picture_filename

def save_post_picture(form_picture):
    random_name = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pictures', picture_filename)
    form_picture.save(picture_path)
    return picture_filename

###########ROUTES#############

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    #for the sidebar
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)

    #for the main part
    posts = Post.query.all()
    posts.reverse()
    comments = Comment.query.all()

    if request.method == 'POST':
        #functionality for the Comment Form
        if 'comment' in request.form:
            post_id = request.form['comment']
            content = request.form['content']
            new_comment = Comment(content=content,
                                  user_id=current_user.id,
                                  post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('home'))
        #functionality for the Like Button
        elif "Like" in request.form:
            post_id = request.form["Like"]
            post = Post.query.filter_by(id=post_id).first()
            post.number_of_likes += 1
            db.session.commit()
        #functionality for the 'View all comments' Button
        elif 'CC' in request.form:
            post_id = request.form['CC']
            comments = Comment.query.filter_by(post_id=post_id)
            return render_template('comments.html', comments=comments)


    return render_template('home.html', posts=posts, image_file=image_file)



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    #section to adjust the pucture
    path = os.path.dirname(__file__)
    full_image_path = f'{path}/static/profile_pictures/{current_user.image_file}'
    picture_x = get_picture_x(full_image_path)
    #
    posts = current_user.route_posts
    return render_template('profile.html', image_file=image_file, picture_x=picture_x,
                           posts=posts)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.aircraft_type = form.aircraft_type.data
        current_user.home_airport = form.home_airport.data
        current_user.name = form.name.data
        current_user.biography = form.biography.data
        db.session.commit()

        flash('Your account has been updated', 'success')
        return redirect(url_for('profile'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.aircraft_type.data = current_user.aircraft_type
        form.home_airport.data = current_user.home_airport
        form.name.data = current_user.name
        form.biography.data = current_user.biography

    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('edit_profile.html', image_file=image_file, form=form)





@app.route('/add_route', methods=['GET', 'POST'])
@login_required
def add_route():
    form = PostForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            new_post = Post(description=form.description.data, image=picture_file,
                                departure_date=form.departure_date.data,
                                departure=form.departure.data, plane=form.plane.data,
                                author=current_user, waypoints=form.waypoints.data,
                                destination=form.destination.data,
                                landing_date=form.landing_date.data)
        else:
            new_post = Post(description=form.description.data,
                    departure_date=form.departure_date.data,
                    departure=form.departure.data, plane=form.plane.data,
                    author=current_user, waypoints=form.waypoints.data,
                    destination=form.destination.data,
                    landing_date=form.landing_date.data)

        db.session.add(new_post)
        db.session.commit()

        flash('Your Post has been uploaded!', 'succsess')
        return redirect(url_for('home'))


    return render_template('add_route.html', form=form)
