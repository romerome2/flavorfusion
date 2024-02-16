from flask import Flask, render_template, request, redirect, url_for, g
import pymysql
import pymysql.cursors
import flask_login
from datetime import datetime

app = Flask(__name__)

app.secret_key = "djfnsdijndf"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, id, username):
        self.username = username
        self.id = id

    def get_id(self):
        return str(self.id)


def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="jspooner",
        password="243565207",
        database="jspooner_erdiagram",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''
    if hasattr(g, 'db'):
        g.db.close()


@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `ID` = {user_id}")
    result = cursor.fetchone()

    if result is None:
        return None

    return User(result["ID"], result["username"])


@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')

    return render_template('register.html.jinja')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["psw"]
        email = request.form["email"]

        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users` (`Username`, `Password`, `Email`) VALUES ('{username}', '{password}', '{email}')")
        cursor.close()
        get_db().commit()

        return redirect('/login')

    if flask_login.current_user.is_authenticated:
        return redirect('/feed')

    return render_template("register.html.jinja")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['psw']

        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE `username` = '{username}'")
        user = cursor.fetchone()

        if user and user['Password'] == password:
            user_obj = User(user['ID'], user['username'])
            flask_login.login_user(user_obj)
            return redirect('/feed')
        else:
            return render_template('login.html.jinja', error='Invalid username or password')

    if flask_login.current_user.is_authenticated:
        return redirect('/feed')

    return render_template('login.html.jinja', error=None)


@app.route('/feed', methods=['GET', 'POST'])
@flask_login.login_required
def feed():
    cursor = get_db().cursor()

    if request.method == 'POST':
        post_content = request.form.get('post_content')
        user_id = flask_login.current_user.id
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO `Posts` (`UserId`, `description`, `Timestamp`) VALUES (%s, %s, %s)",
                       (user_id, post_content, timestamp))
        get_db().commit()

    cursor.execute("SELECT * FROM `Posts`")
    posts = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja", posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
