from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors
import flask_login



app = Flask(__name__)

app.secret_key ="djfnsdijndf"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
class User:
     is_aunthenticated =True
     is_anonymous = False
     is_active = True
     def __init__(self,id,username):
      self.username = username
      self.id = id
     def get_id(self):
             return str(self.id)

def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `users`WHERE `id` = "+str(user_id))
    result = cursor.fetchone()
    if result is None:
        return None
    return User(result["id"], result["username"])

  
conn = pymysql.connect(
    database="jspooner_erdiagram" ,
    user="jspooner",
    password="243565207",
    host="10.100.33.60",
    cursorclass=pymysql.cursors.DictCursor,
)

@login_manager.user_loader
def load_user(user_id):
    Cursor = conn.cursor()
    Cursor.execute(f"SELECT * FROM `Users`Where` `ID` = " + user_id)
    result = Cursor.fetchone()
    Cursor.close()
    conn.commit()
   
@app.route('/')
def index():
    return render_template('home.html.jinja')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        bio = request.form["bio"]
        birthday = request.form["birthday"]
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `user` (__PUT_COLUMNS_HERE__) VALUES ('{username}', '{password}', '{bio}')")
    cursor.close()
    conn.commit()
    
    return render_template("register.html.jinja")
 
