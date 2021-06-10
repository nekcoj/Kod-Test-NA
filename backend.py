from flask import Flask, jsonify, request, g
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

DATABASE = 'database.db'

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'Th1sIs4s3crE7'

# routes
@app.route('/api/login', methods=['GET', 'POST'])
def login():
  
  if request.method == 'GET':
    message = {'greeting':'Hello from login!'}
    return jsonify(message)

  if request.method == 'POST':
    data = request.get_json()
    return loginUser(data)

def loginUser(data):
  con = get_db()
  user = {}
  try:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (data["email"], ))
    users = cur.fetchall()
    for u in users:
      if check_password_hash(u[1], data['password']):
        user_data = {}
        user_data['user_id'] = u[5]
        user_data['token'] = encode_auth_token(u[0])
        updateUser(u[1], datetime.now(), u[4]+1, user_data['token'], u[5])
        user = user_data
      else:
        user =  { 'message': 'Incorrect email/password' }
  except:
    con.rollback()
    return "Failed", 400
  finally:
    con.close()
    return jsonify(user), 200
  
def updateUser(password, last_login, number_of_logins, token, user_id):
  con = get_db()
  try:
    cur = con.cursor()
    cur.execute('UPDATE users SET password=?, last_login=?, number_of_logins=?, token=? WHERE user_id=?', (password, last_login, number_of_logins, token, user_id))
    con.commit()
  except Exception as e:
    print('UPDATE? NOPE!', e)
    con.rollback()
  finally:
    return

@app.route('/api/register', methods = ['POST'])
def register_user():
  if request.method == 'POST':
    con = get_db()
    try:
      data = request.get_json()
      created = datetime.now()
      email = data["email"]
      password = generate_password_hash(data["password"], method='sha256')
      with con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (email, password, created) VALUES (?,?,?)", (email, password, created))
        con.commit()
        msg = {'message': "Account created successfully"}, 200
    except:  
      con.rollback()
      msg = {'error': "Error, cannot create account"}, 400
    finally:
      con.close()
      return msg

# database
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

# JWT
def encode_auth_token(email):
  try:
    payload = {
      'exp': datetime.utcnow() + timedelta(days=0, seconds=900),
      'iat': datetime.utcnow(),
      'sub': email
    }
    return jwt.encode(
      payload,
      app.config['SECRET_KEY'],
      algorithm='HS256'
    )
  except Exception as e:
    return e