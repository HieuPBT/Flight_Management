from datetime import date

from flask import redirect, request
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_login import logout_user, login_required, login_user, current_user
from flightapp import app, db, dao
from models import *


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class SanBayView(AuthenticatedView):
    column_list = ['id', 'ten', 'tinh']
    column_searchable_list = ['ten', 'tinh']
    column_filters = ['ten', 'tinh']
    column_labels = {
        'id': "id",
        'ten': 'Tên sân bay',
        'tinh': "Tỉnh"
    }


class TuyenBayView(AuthenticatedView):
    column_list = ['id', 'san_bay_di', 'san_bay_den']
    # column_searchable_list = ['ten', 'tinh']
    # column_filters = ['ten', 'tinh']
    column_labels = {
        'id': "id",
        'san_bay_den': 'Sân bay đến',
        'san_bay_di': 'Sân bay đi'
    }


class QuyDinhView(AuthenticatedView):
    pass


class LapLichView(AuthenticatedView):
    column_list = ['id', 'ngay_gio_khoi_hanh', 'thoi_gian_bay', 'may_bay.ten']
    # column_searchable_list = ['ten', 'tinh']
    # column_filters = ['ten', 'tinh']
    column_labels = {
        'id': "id",
        'ngay_gio_khoi_hanh': 'Ngày - giờ khởi  hành',
        'thoi_gian_bay': "Thời gian bay",
        'may_bay.ten': "Máy bay",
    }


class CustomLapLichView(AuthenticatedView):
    @expose('/create_flight_schedule/', methods=('GET', 'POST'))
    # create_template = 'flight_schedule.html'
    def create_view(self):
        return self.render('flight_schedule.html')


class StatsView(BaseView):
    @login_required
    @expose('/')
    def index(self):
        revenue_by_route = dao.stats_route_revenue()
        total = 0
        for i in revenue_by_route:
            total += i[2]
        return self.render('admin/stats.html', revenue_by_route=revenue_by_route, total=total)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name="Quản Lý Chuyến Bay", template_mode="bootstrap4")
admin.add_view(SanBayView(SanBay, db.session, name="Sân Bay"))
admin.add_view(TuyenBayView(TuyenBay, db.session, name="Tuyến Bay"))
admin.add_view(QuyDinhView(QuyDinh, db.session, name="Quy Định"))
admin.add_view((CustomLapLichView(ChuyenBay, db.session, name="Lập Lịch Chuyến Bay")))
admin.add_view(ModelView(MayBay, db.session, name="Máy Bay"))
admin.add_view(ModelView(User, db.session, name="Máy Bay"))
admin.add_view(StatsView(name="Thống Kê", endpoint='Stats'))
admin.add_view(LogoutView(name="Đăng Xuất"))

