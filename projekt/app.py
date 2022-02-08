from flask import Flask, render_template, request


app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
