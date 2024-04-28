from flask import redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, login_required, login_user

from flightapp import app, db
from models import *


class StatsView(BaseView):
    @login_required
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app, name="Quản Lý Chuyến Bay", template_mode="bootstrap4")
admin.add_view(ModelView(SanBay, db.session, name="Sân Bay"))
admin.add_view(ModelView(QuyDinh, db.session, name="Quy Định"))
admin.add_view((ModelView(ChuyenBay, db.session, name="Lập Lịch Chuyến Bay")))
admin.add_view(StatsView(name="Thống Kê"))
admin.add_view(LogoutView(name="Đăng Xuất"))

