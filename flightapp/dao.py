from datetime import timedelta

from models import *
from flask_login import current_user
import hashlib
from sqlalchemy import func
from flightapp import utils


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


def count_tickets_sold_by_hvcb_id(hang_ve_chuyen_bay_id):
    return (db.session.query(func.count(Ve.id))
            .join(HangVeChuyenBay, Ve.hang_ve_chuyen_bay_id.__eq__(HangVeChuyenBay.id))
            .filter(HangVeChuyenBay.id.__eq__(hang_ve_chuyen_bay_id)).all())[0][0]


def get_available_flights(departure, destination, ticket_class, passengers, leave_date):
    leave_date = datetime.strptime(leave_date, "%Y-%m-%d").date()
    flight_time = get_flight_time(ChuyenBay.id)
    flight_time_td = timedelta(minutes=flight_time)

    current_time = datetime.now()
    cutoff_time = current_time - timedelta(minutes=
                                           load_config(QuyDinhKey.SOLDTIME).value
                                           if current_user.user_role == UserRole.TICKET_SELLER
                                           else load_config(QuyDinhKey.BOOKINGTIME).value)

    print(cutoff_time)

    return ((db
            .session
            .query(func.TIME(ChuyenBay.ngay_gio_khoi_hanh), HangVeChuyenBay.gia, TuyenBay, HangVe.ten, func.TIME(flight_time_td), HangVeChuyenBay.id)
            .join(HangVe, HangVeChuyenBay.hang_ve_id.__eq__(HangVe.id), isouter=True)
            .join(ChuyenBay, HangVeChuyenBay.chuyen_bay_id.__eq__(ChuyenBay.id), isouter=True)
            .join(TuyenBay, TuyenBay.id.__eq__(ChuyenBay.tuyen_bay_id), isouter=True))
            .filter(HangVe.id.__eq__(ticket_class)
                    & func.TIME(ChuyenBay.ngay_gio_khoi_hanh) < func.TIME(cutoff_time)
                    & TuyenBay.san_bay_di_id.__eq__(departure)
                    & TuyenBay.san_bay_den_id.__eq__(destination)
                    & func.DATE(ChuyenBay.ngay_gio_khoi_hanh).__eq__(leave_date)
                    & (HangVeChuyenBay.so_luong - count_tickets_sold_by_hvcb_id(HangVeChuyenBay.id)).__ge__(passengers)
                    ).all())


def get_flight_time(flight_id):
    return db.session.query(ChuyenBay.thoi_gian_bay, ChuyenBay.id.__eq__(flight_id)).first()[0]


def get_available_seats(hang_ve_chuyen_bay_id):
    all_seats = (db.session.query(Ghe)
                 .join(GheMayBay, Ghe.id.__eq__(GheMayBay.ghe_id))
                 .join(MayBay, MayBay.id.__eq__(GheMayBay.may_bay_id))
                 .join(ChuyenBay, ChuyenBay.may_bay_id.__eq__(MayBay.id))
                 .join(HangVeChuyenBay, HangVeChuyenBay.chuyen_bay_id.__eq__(ChuyenBay.id))
                 .join(HangVe, HangVe.id.__eq__(GheMayBay.hang_ve_id) & HangVe.id.__eq__(HangVeChuyenBay.hang_ve_id))
                 .filter(HangVeChuyenBay.id.__eq__(hang_ve_chuyen_bay_id))).all()
    booked_seats = (db.session.query(Ghe)
                    .join(GheMayBay, Ghe.id.__eq__(GheMayBay.ghe_id))
                    .join(Ve, Ve.ghe_may_bay_id.__eq__(GheMayBay.id))
                    .join(HangVeChuyenBay, HangVeChuyenBay.id.__eq__(Ve.hang_ve_chuyen_bay_id))
                    .filter(HangVeChuyenBay.id.__eq__(hang_ve_chuyen_bay_id)).all())
    booked_seat_ids = {seat.id for seat in booked_seats}

    for seat in all_seats:
        seat.available = seat.id not in booked_seat_ids

    return all_seats


def get_seat_plane(ghe_id, hang_ve_chuyen_bay_id):
    return (db.session.query(GheMayBay)
            .join(MayBay, MayBay.id.__eq__(GheMayBay.may_bay_id))
            .join(ChuyenBay, ChuyenBay.may_bay_id.__eq__(MayBay.id))
            .join(HangVeChuyenBay, HangVeChuyenBay.chuyen_bay_id.__eq__(ChuyenBay.id))
            .filter(GheMayBay.ghe_id.__eq__(ghe_id) & HangVeChuyenBay.id.__eq__(hang_ve_chuyen_bay_id)).first())


def add_ticket(ghe_may_bay_id, hang_ve_chuyen_bay_id, khach_hang_id):
    ticket = Ve(ghe_may_bay_id=ghe_may_bay_id, hang_ve_chuyen_bay_id=hang_ve_chuyen_bay_id, khach_hang_id=khach_hang_id)
    db.session.add(ticket)
    db.session.commit()


def get_info(identity=None, phone_number=None):
    session = db.session
    info = session.query(ThongTinNguoiDung).filter((ThongTinNguoiDung.CCCD == identity) | (ThongTinNguoiDung.so_dien_thoai == phone_number)).first()
    return info


def get_ticket():
    return Ve.query.all()


def add_user_info(name, phone_number, address, identity, email):
    info = get_info(identity, phone_number)
    if info is None:
        info = ThongTinNguoiDung(ho_va_ten=name, so_dien_thoai=phone_number, dia_chi=address, email=email, CCCD=identity)
        db.session.add(info)
        db.session.commit()
        return info
    else:
        return info


def get_route_by_id(route_id):
    return TuyenBay.query.get(route_id)


def stats_flight_revenue_by_route_id(route_id):
    return (db.session.query(ChuyenBay, HangVeChuyenBay.gia * func.count(Ve.id), func.count(ChuyenBay.id))
            .join(Ve, Ve.hang_ve_chuyen_bay_id.__eq__(HangVeChuyenBay.id), isouter=True)
            .join(ChuyenBay, ChuyenBay.id.__eq__(HangVeChuyenBay.chuyen_bay_id))
            .join(TuyenBay, TuyenBay.id.__eq__(ChuyenBay.tuyen_bay_id))
            .group_by(HangVeChuyenBay.chuyen_bay_id, HangVeChuyenBay.gia).filter(TuyenBay.id.__eq__(route_id)).all())


def stats_route_revenue(year=datetime.now().year, month=datetime.now().month):
    subquery = (db.session
                .query(TuyenBay.id.label('tuyen_bay_id'), (HangVeChuyenBay.gia * func.count(Ve.id)).label('total_price'))
                .join(Ve, Ve.hang_ve_chuyen_bay_id.__eq__(HangVeChuyenBay.id), isouter=True)
                .join(ChuyenBay, ChuyenBay.id.__eq__(HangVeChuyenBay.chuyen_bay_id))
                .join(TuyenBay, TuyenBay.id.__eq__(ChuyenBay.tuyen_bay_id))
                .group_by(TuyenBay.id, HangVeChuyenBay.gia)
                .filter(func.extract('year', ChuyenBay.created_date).__eq__(year))
                .filter(func.extract('month', ChuyenBay.created_date).__eq__(month))
                .subquery())

    query = (db.session.query(subquery.c.tuyen_bay_id, func.sum(subquery.c.total_price))
             .group_by(subquery.c.tuyen_bay_id)
             .all())
    modified_results = []
    for q in query:
        tuyen_bay_id = q[0]
        total_price = q[1]
        route = get_route_by_id(tuyen_bay_id)
        modified_results.append((route, total_price))
    flight_counts = (db.session.query(TuyenBay.id, func.count(ChuyenBay.id))
                     .join(TuyenBay, TuyenBay.id.__eq__(ChuyenBay.tuyen_bay_id))
                     .group_by(TuyenBay.id)
                     .all())

    merged_results = []
    for tuyen_bay_id, flight_count in flight_counts:
        for route, total_price in modified_results:
            if route.id == tuyen_bay_id:
                merged_results.append((route.id, str(route), total_price, flight_count))
                break

    return merged_results


def stats_route_flight_count():
    return (db.session.query(TuyenBay.id, func.count(ChuyenBay.id))
            .join(TuyenBay, TuyenBay.id.__eq__(ChuyenBay.tuyen_bay_id))).group_by(TuyenBay.id).all()

# def stats_


def add_user(name, username, password, email, cccd, phone_number, address):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user_info = add_user_info(name, phone_number, address, cccd, email)
    u = User(username=username, password=password)
    user_info.tai_khoan_id = u.id
    db.session.add_all([u, user_info])
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


if __name__ == '__main__':
    with app.app_context():
        print(stats_route_revenue(2024, 5))