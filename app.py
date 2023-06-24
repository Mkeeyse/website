from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.secret_key = 'qwertyuio'

# Establish a connection to the database
engine = create_engine(   "mysql+mysqlconnector://642ky6svrnizgbjw53hg:pscale_pw_oqbUdqC2dOCT8CLH2XmWC2wydOeA4NH68tC5r0TCTSC@aws.connect.psdb.cloud/file_system?ssl_ca=/etc/ssl/cert.pem"
)

@app.route("/")
def hello_world():
    return render_template("login.html")

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
            return redirect(url_for('home'))
        else:
            msg = "Invalid username or password. Please try again."

    return render_template('login.html', msg=msg)

@app.route('/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
