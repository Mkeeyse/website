from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models.file import File
from models.login import User
from database import get_user_info
from database import login_user



import os

# Initialize database connection

# Retrieve the database connection string from an environment variable
db_conn = os.getenv('DB_CONN')

# Remove unwanted quotes from the db_conn variable
if db_conn is not None:
    db_conn = db_conn.replace('"', '')

print("DB_CONN:", repr(db_conn))

if db_conn is None:
    print("DB_CONN environment variable is not set.")
else:
    # Establish a connection to the database
    engine = create_engine(db_conn)



app = Flask(__name__)
app.secret_key = 'qwertyuio'


# ...



# ...

def db_login_user(user_name, user_password):
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter_by(user_name=user_name).first()
    if user and user.check_password(user_password):
        return user.to_dict()
    else:
        return None





def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session or not session['is_admin']:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        record = login_user(username, password)

        if record:
            session['loggedin'] = True
            session['username'] = record['username']
            session['id'] = record['id']  # Store the user_id in the session
            session['is_admin'] = record['is_admin']  # Store the admin status in the session
            if session['is_admin']:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            msg = "Invalid username or password. Please try again."

    return render_template('login.html', msg=msg)


@app.route('/home')
@login_required
def home():
    user_info = get_user_info(session['id'])

    if user_info:
        return render_template('home.html', user_info=user_info)
    else:
        return "User information not found."

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        record = login_user(username, password)

        if record and record['is_admin']:  # Check if user exists and is an admin
            session['loggedin'] = True
            session['username'] = record['username']
            session['id'] = record['id']  # Store the user_id in the session
            session['is_admin'] = record['is_admin']  # Store the admin status in the session
            return redirect(url_for('admin'))
        else:
            msg = "Invalid username or password. Please try again."

    return render_template('admin_login.html', msg=msg)

@app.route('/admin')
@admin_required
def admin():
    users = get_user_info(session['id'])

    return render_template('admin.html', user_info=users)


@app.route('/files')
@login_required
def files():
    connection = engine.connect()
    statement = text("SELECT * FROM file")
    result = connection.execute(statement)
    files = result.fetchall()
    connection.close()

    return render_template('files.html', files=files)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
