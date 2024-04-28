from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flightapp import app, db

admin = Admin(app, name="Quan ly chuyen bay", template_mode="bootstrap4")


