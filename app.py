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







#######################################
# 
@app.route('/file_table', methods=['POST'])
def add_file():
    if request.method == 'POST':
        # Handle the JSON data here
        data = request.get_json()
        print(data)

        category = data.get('category')
        ref_num = data.get('ref_num')
        title = data.get('title')
        status = data.get('status')

        if category is None or ref_num is None or title is None or status is None:
            # Handle the case where any of the required fields are missing
            return "Missing required form fields", 400

        # Create a new File object with the data
        file = File(
            category=category,
            ref_num=ref_num,
            title=title,
            status=status
        )

        # Connect to the database and add the new file record
        session = Session()
        session.add(file)
        session.commit()
        session.close()

        # Debug the JSON data
        print(data)

        # Redirect to another page after successful submission
        return redirect(url_for('files'))

    # Render the HTML template
    return render_template('file_table.html')

#######################################

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
