from models import *
import hashlib


def load_sanbay():
    return SanBay.query.all()


def load_hangve():
    return HangVe.query.all()


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
