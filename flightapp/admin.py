from datetime import date

from flask import redirect, request
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_login import logout_user, login_required, login_user, current_user
from flightapp import app, db, dao
from flightapp.models import *


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


def format_enum_value(view, context, model, name):
    enum_value = getattr(model, name)
    if isinstance(enum_value, QuyDinhKey):
        return enum_value.value  # Change to enum_value.name if you want to display the name
    return enum_value


class QuyDinhView(AuthenticatedView):
    can_delete = False
    can_create = False
    column_list = ['key', 'value', 'created_date', 'nhan_vien_quan_tri']

    column_formatters = {
        'key': format_enum_value
    }
    form_excluded_columns = ['created_date', 'nhan_vien_quan_tri']
    column_labels = {
        'key': 'Tên Quy Định',
        'value': 'Giá Trị',
        'active': 'Hoạt Động',
        'created_date': 'Ngày Thay Đổi Gần Nhất',
        'nhan_vien_quan_tri': 'Nhân Viên Quản Trị'
    }

    def on_model_change(self, form, model, is_created):
        model.created_date = datetime.now()
        model.nhan_vien_quan_tri_id = current_user.id


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
        current_month = datetime.now().month
        current_year = datetime.now().year
        total = 0
        for i in revenue_by_route:
            total += i[2]
        return self.render('admin/stats.html', revenue_by_route=revenue_by_route, total=total, current_month=current_month, current_year=current_year)

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
admin.add_view(StatsView(name="Thống Kê", endpoint='Stats'))
admin.add_view(LogoutView(name="Đăng Xuất"))

