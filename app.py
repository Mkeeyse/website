from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
from database import engine, login_user, get_user_info

app = Flask(__name__)
app.secret_key = 'qwertyuio'

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
    users = get_user_info()

    return render_template('admin.html', users=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
