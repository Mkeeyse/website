from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import create_engine, text
from functools import wraps

app = Flask(__name__)
app.secret_key = 'qwertyuio'

# Establish a connection to the database
engine = create_engine("mysql+mysqlconnector://642ky6svrnizgbjw53hg:pscale_pw_oqbUdqC2dOCT8CLH2XmWC2wydOeA4NH68tC5r0TCTSC@aws.connect.psdb.cloud/file_system?ssl_ca=/etc/ssl/cert.pem")

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

        # Execute the login query
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * FROM User WHERE user_name = :username AND user_password = :password"),
                {"username": username, "password": password}
            )
            record = result.fetchone()

        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            session['id'] = record[0]  # Store the user_id in the session
            session['is_admin'] = record[5]  # Store the admin status in the session
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
    # Retrieve user information from the server/database
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM User WHERE id = :user_id"),
            {"user_id": session['id']}
        )
        record = result.fetchone()

    if record:
        user_info = {
            'username': record[1],
            'department': record[4],
            'email': record[2],
        }
        return render_template('home.html', user_info=user_info)
    else:
        return "User information not found."

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        # Execute the login query
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * FROM User WHERE user_name = :username AND user_password = :password"),
                {"username": username, "password": password}
            )
            record = result.fetchone()

        if record and record[5]:  # Check if user exists and is an admin
            session['loggedin'] = True
            session['username'] = record[1]
            session['id'] = record[0]  # Store the user_id in the session
            session['is_admin'] = record[5]  # Store the admin status in the session
            return redirect(url_for('admin'))
        else:
            msg = "Invalid username or password. Please try again."

    return render_template('admin_login.html', msg=msg)

@app.route('/admin')
@admin_required
def admin():
    # Retrieve all users from the server/database
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM User")
        )
        users = result.fetchall()

    return render_template('admin.html', users=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
