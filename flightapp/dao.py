from models import *
from flask_login import current_user
import hashlib


def add_flight_schedule(depart, depart_date_time, flight_duration, plane, ticket_class_data, im_airport):
    f = ChuyenBay(ngay_gio_khoi_hanh=depart_date_time, thoi_gian_bay=flight_duration,
                  tuyen_bay_id=depart, may_bay_id=plane, nhan_vien_quan_tri_id=current_user.id)

    db.session.add(f)
    db.session.flush()

    for c in ticket_class_data:
        h = HangVeChuyenBay(hang_ve_id=c['ticketClass'], so_luong=c['quantity'], gia=c['ticketPrice'],
                            chuyen_bay_id=f.id)
        db.session.add(h)

    for s in im_airport:
        a = SanBayTrungGian(san_bay_id=s['airportId'], chuyen_bay_id=f.id, thoi_gian_dung=s['duration'], note=s['note'])

        db.session.add(a)

    db.session.commit()


def load_plane():
    return MayBay.query.all()


def load_flight_route():
    return TuyenBay.query.all()


def load_config(enum):
    return QuyDinh.query.filter(QuyDinh.key.__eq__(enum)).first()


def load_airport():
    return SanBay.query.all()


def load_ticket_class():
    return HangVe.query.all()


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
