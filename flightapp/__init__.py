from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key = '8s6tx8a(*&9y(^xuuiyg8y&(u0^&^TG*76*&T8YG*^T*g8'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/flightdb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['key2'] = 'kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nxloc2701@gmail.com'
app.config['MAIL_PASSWORD'] = 'aimwnbmlhottouep'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
login = LoginManager(app)
CORS(app)
mail = Mail(app)
