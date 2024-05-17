from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = '8s6tx8a(*&9y(^xuuiyg8y&(u0^&^TG*76*&T8YG*^T*g8'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/flightdb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app)
login = LoginManager(app)
CORS(app)
