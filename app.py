# app.py
from flask import Flask, render_template, request, session, redirect, url_for
import os
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.login import User
from models.file import File

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'qwertyuio'

# Configure the database connection
db_conn = os.getenv('DB_CONN')
if db_conn is None:
    print("DB_CONN environment variable is not set.")
else:
    db_conn = db_conn.replace('"', '')
    engine = create_engine(db_conn)
    Session = sessionmaker(bind=engine)


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Route for the home page
@app.route("/")
def hello_world():
    return render_template("login.html")


# Route for user logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        # Perform user authentication here
        # ...

        session['loggedin'] = True
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('login.html')


# Route for the user's home page
@app.route('/home')
@login_required
def home():
    user_info = {
        'username': session['username'],
        # Add other user information as needed
    }
    return render_template('home.html', user_info=user_info)


# Route for the files page
@app.route('/files')
@login_required
def files():
    # Connect to the database and retrieve all records from the File table
    session = Session()
    files = session.query(File).all()
    session.close()

    return render_template('files.html', files=files)


# Route for adding a file
@app.route('/add-file', methods=['POST'])
@login_required
def add_file():
    # Extract file information from the request form
    file_number = request.form.get('file_number')
    date_added = request.form.get('date_added')
    category = request.form.get('category')
    ref_num = request.form.get('ref_num')
    title = request.form.get('title')
    status = request.form.get('status')

    # Perform file addition logic here
    # ...

    return "File added successfully."


# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
