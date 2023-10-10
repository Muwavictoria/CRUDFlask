from flask import render_template, request, redirect, url_for, session
from Accounts import app
from Accounts import mysql
import MySQLdb.cursors, hashlib
import re


@app.route("/")
def home_page():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    # return render_template("home.html")


#
# @app.route("/home", endpoint="home_alternate")
# def home_page():
#     return render_template("home.html")


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('logged in', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password

            hash_password = password + app.secret_key
            hash_password = hashlib.sha1(hash_password.encode())
            password = hash_password.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
    #     username = request.form['username']
    #     password = request.form['password']
    #     email = request.form['email']
    #
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM user WHERE username= % s', (username,))
    #     user = cursor.fetchone()
    #
    #     print("User from database:", user)
    #
    #     if user:
    #         msg = 'User already exits !'
    #     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #         msg = 'Invalid email address !'
    #     elif not re.match(r'[A-Za-z0-9]+', username):
    #         msg = 'Username must contain only characters and numbers !'
    #     elif not username or not password or not email:
    #         msg = 'Please in the missing Values !'
    #     else:
    #         cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, password, email,))
    #         mysql.connection.commit()
    #         msg = 'You have successfully registered !'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    # return render_template("register.html", msg=msg)


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ""
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Retrieve the hashed password
        hash_password = password + app.secret_key
        hash_password = hashlib.sha1(hash_password.encode())
        password = hash_password.hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account does not exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # msg = ''
    # if request.method == "POST" and "username" in request.form and 'password' in request.form:
    #     username = request.form['username']
    #     password = request.form['password']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute("SELECT * FROM user WHERE username = % s AND password= % s", (username, password))
    #     account = cursor.fetchone()
    #     if account:
    #         session['logged in'] = True
    #         session['id'] = account['id']
    #         session['username'] = account['username']
    #         msg = 'Logged in successfully !'
    #         return redirect('url_for("home_page")')
    #     else:
    #         msg = 'Incorrect username / password !'
    # Show the login form with message (if any)
    return render_template("home.html", msg=msg)
