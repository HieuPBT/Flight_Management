from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from flightapp import db, app
from flask_login import UserMixin
from enum import Enum as RoleEnum
from datetime import datetime


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2
    TICKET_SELLER = 3


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class User(Base, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    thong_tin_nguoi_dung = relationship('ThongTinNguoiDung', backref='user', lazy=False, uselist=False)
    quy_dinh = relationship('QuyDinh', foreign_keys='QuyDinh.nhan_vien_quan_tri_id', backref='nhan_vien_quan_tri', lazy=True)

    def __str__(self):
        return self.username


class ThongTinNguoiDung(Base):
    ho_va_ten = Column(String(50), nullable=False)
    so_dien_thoai = Column(String(20))
    dia_chi = Column(String(255))
    email = Column(String(50))
    CCCD = Column(String(20))
    tai_khoan_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    ve = relationship('Ve', foreign_keys='Ve.khach_hang_id', backref='thong_tin_nguoi_dung', lazy=True)


class SanBay(Base):
    ten = Column(String(50), nullable=False)
    tinh = Column(String(100), nullable=False)
    # tuyen_bay_di = relationship('TuyenBay', foreign_keys='TuyenBay.san_bay_di_id', backref='san_bay_di', lazy=True)
    # tuyen_bay_den = relationship('TuyenBay', foreign_keys='TuyenBay.san_bay_den_id', backref='san_bay_den', lazy=True)
    san_bay_trung_gian = relationship('SanBayTrungGian', backref='san_bay', lazy=True)

    def __str__(self):
        return self.ten


class TuyenBay(Base):
    san_bay_di_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    san_bay_den_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    san_bay_di = relationship('SanBay', foreign_keys=[san_bay_di_id], backref='tuyen_bay_di', lazy=True)
    san_bay_den = relationship('SanBay', foreign_keys=[san_bay_den_id], backref='tuyen_bay_den', lazy=True)
    #chuyen_bay = relationship('ChuyenBay', backref='tuyen_bay', lazy=True)

    def __str__(self):
        return f"{self.san_bay_di} - {self.san_bay_den}"


class Ghe(Base):
    ten = db.Column(db.String(5), nullable=False)
    ghe_may_bay = relationship('GheMayBay', backref='ghe', lazy=True)


class MayBay(Base):
    ten = Column(String(20), nullable=False)
    ghe_may_bay = relationship('GheMayBay', backref='may_bay', lazy=True)
    # chuyen_bay = relationship('ChuyenBay', backref='may_bay', lazy=True)


class HangVe(Base):
    ten = Column(String(20), nullable=False)
    hang_ve_chuyen_bay = relationship('HangVeChuyenBay', backref='hang_ve', lazy=True)


class ChuyenBay(Base):
    ngay_gio_khoi_hanh = Column(DateTime, nullable=False)
    thoi_gian_bay = Column(Integer, nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey('tuyen_bay.id'), nullable=False)
    tuyen_bay = relationship('TuyenBay', foreign_keys=[tuyen_bay_id], lazy=True)
    nhan_vien_quan_tri_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    may_bay_id = Column(Integer, ForeignKey('may_bay.id'), nullable=False)
    may_bay = relationship('MayBay', foreign_keys=[may_bay_id], lazy=True)
    san_bay_trung_gian = relationship('SanBayTrungGian', backref='chuyen_bay', lazy=True)


class HangVeChuyenBay(Base):
    hang_ve_id = Column(Integer, ForeignKey('hang_ve.id'), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey('chuyen_bay.id'), nullable=False)
    so_luong = Column(Integer, nullable=False) #số lượng hạng vé này trên chuyến bay này
    gia = Column(Integer, nullable=False)
    ve = relationship('Ve', backref='hang_ve_chuyen_bay', lazy=True)
    __table_args__ = (
        UniqueConstraint('hang_ve_id', 'chuyen_bay_id'),
    )


class GheMayBay(Base):
    ghe_id = Column(Integer, ForeignKey('ghe.id'), nullable=False)
    may_bay_id = Column(Integer, ForeignKey('may_bay.id'), nullable=False)
    ve = relationship('Ve', backref='ghe_may_bay', lazy=True)
    __table_args__ = (
        UniqueConstraint('ghe_id', 'may_bay_id'),
    )


class Ve(Base):
    ghe_may_bay_id = Column(Integer, ForeignKey('ghe_may_bay.id'), nullable=False)
    hang_ve_chuyen_bay_id = Column(Integer, ForeignKey('hang_ve_chuyen_bay.id'), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey('thong_tin_nguoi_dung.id'), nullable=False)
    hoa_don_id = Column(Integer, ForeignKey('hoa_don.id'), nullable=False)


class HoaDon(Base):
    ve = relationship('Ve', backref='hoa_don', uselist=False, lazy=True)


class SanBayTrungGian(Base):
    san_bay_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey('chuyen_bay.id'), nullable=False)
    thoi_gian_dung = Column(Integer, nullable=False)
    note = Column(String(100), nullable=True)
    __table_args__ = (
        UniqueConstraint('san_bay_id', 'chuyen_bay_id'),
    )


class QuyDinh(Base):
    key = Column(String(50), nullable=False, unique=True)
    value = Column(Integer, nullable=False)
    nhan_vien_quan_tri_id = Column(Integer, ForeignKey('user.id'), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        #
        #
        # u = User(username='admin',
        #          password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)  # Use the ID of the created record
        # db.session.add(u)
        # db.session.commit()
        #
        # info = ThongTinNguoiDung(ho_va_ten="admin", tai_khoan_id=1)
        # info2 = ThongTinNguoiDung(ho_va_ten="Nguyễn Xuân Lộc", so_dien_thoai='0362655091', dia_chi='Gia Lai',
        #                           email='2151013052loc@gmail.com', CCCD='0798723983792')
        # db.session.add_all([info, info2])  # Add and commit information first
        # db.session.commit()
        #
        # sb1 = SanBay(ten='Cà Mau', tinh='Cà Mau')
        # sb2 = SanBay(ten='Cần Thơ', tinh='Cần Thơ')
        # sb3 = SanBay(ten='Đà Nẵng', tinh='Đà Nẵng')
        # sb4 = SanBay(ten='Pleiku', tinh='Pleiku')
        # sb5 = SanBay(ten='Tân Sơn Nhất', tinh='Thành phố Hồ Chí Minh')
        # sb6 = SanBay(ten='Nội Bài', tinh='Hà Nội')
        # sb7 = SanBay(ten='Điện Biên Phủ', tinh='Điện Biên')
        # sb8 = SanBay(ten='Liên Khương', tinh='Lâm Đồng')
        # sb9 = SanBay(ten='Phú Bài', tinh='Thừa Thiên Huế')
        # sb10 = SanBay(ten='Vinh', tinh='Nghệ An')
        #
        #
        # db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10])
        #
        # db.session.commit()
        #
        # tb1 = TuyenBay(san_bay_di_id=5, san_bay_den_id=6)  # HCM - HN
        # tb2 = TuyenBay(san_bay_di_id=5, san_bay_den_id=6)  # HN - HCM
        # tb3 = TuyenBay(san_bay_di_id=1, san_bay_den_id=2)  # Cà Mau - Cần Thơ
        # tb4 = TuyenBay(san_bay_di_id=9, san_bay_den_id=10)  # Hue - Nghệ An
        # db.session.add_all([tb1, tb2, tb3, tb4])
        #
        # db.session.commit()

        # mb1 = MayBay(ten='BOE701')
        # mb2 = MayBay(ten='VietAir234')
        # mb3 = MayBay(ten='AirJet709')
        #
        # g1 = Ghe(ten='A01')
        # g2 = Ghe(ten='A02')
        # g3 = Ghe(ten='B01')
        # g4 = Ghe(ten='C01')
        # g5 = Ghe(ten='B02')
        # g6 = Ghe(ten='A03')
        #
        # db.session.add_all([mb1, mb2, mb3, g1, g2, g3, g4, g5, g6])
        #
        # db.session.commit()

        # g_mb1 = GheMayBay(ghe_id=1, may_bay_id=1)
        # g_mb2 = GheMayBay(ghe_id=2, may_bay_id=1)
        # g_mb3 = GheMayBay(ghe_id=3, may_bay_id=1)
        # g_mb4 = GheMayBay(ghe_id=4, may_bay_id=1)
        # g_mb5 = GheMayBay(ghe_id=5, may_bay_id=1)
        # g_mb6 = GheMayBay(ghe_id=6, may_bay_id=1)
        #
        # db.session.add_all([g_mb1, g_mb2, g_mb3, g_mb4, g_mb5, g_mb6])
        #
        # db.session.commit()

        # hv1 = HangVe(ten='Thương Gia')
        # hv2 = HangVe(ten='Phổ Thông')
        #
        # cb1 = ChuyenBay(ngay_gio_khoi_hanh='2024-5-10', thoi_gian_bay=200, tuyen_bay_id=1,
        #                 nhan_vien_quan_tri_id=1, may_bay_id=1)
        #
        # db.session.add_all([hv1, hv2, cb1])
        #
        # db.session.commit()


