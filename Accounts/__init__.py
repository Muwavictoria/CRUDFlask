from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = 'your secret key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/accounts'
# db = SQLAlchemy(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "accounts"


mysql = MySQL(app)


from Accounts import routes


