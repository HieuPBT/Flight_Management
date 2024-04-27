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
    tuyen_bay_di = relationship('TuyenBay', foreign_keys='TuyenBay.san_bay_di_id', backref='san_bay_di', lazy=True)
    tuyen_bay_den = relationship('TuyenBay', foreign_keys='TuyenBay.san_bay_den_id', backref='san_bay_den', lazy=True)
    san_bay_trung_gian = relationship('SanBayTrungGian', backref='san_bay', lazy=True)


class TuyenBay(Base):
    san_bay_di_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    san_bay_den_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    chuyen_bay = relationship('ChuyenBay', backref='tuyen_bay', lazy=True)


class Ghe(Base):
    ten = db.Column(db.String(5), nullable=False)
    ghe_may_bay = relationship('GheMayBay', backref='ghe', lazy=True)


class MayBay(Base):
    ten = Column(String(20), nullable=False)
    ghe_may_bay = relationship('GheMayBay', backref='may_bay', lazy=True)
    chuyen_bay = relationship('ChuyenBay', backref='may_bay', lazy=True)


class HangVe(Base):
    ten = Column(String(20), nullable=False)
    hang_ve_chuyen_bay = relationship('HangVeChuyenBay', backref='hang_ve', lazy=True)


class ChuyenBay(Base):
    ngay_gio_khoi_hanh = Column(DateTime, nullable=False)
    thoi_gian_bay = Column(Integer, nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey('tuyen_bay.id'), nullable=False)
    nhan_vien_quan_tri_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    may_bay_id = Column(Integer, ForeignKey('may_bay.id'), nullable=False)
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
    ve_id = Column(Integer, ForeignKey('ve.id'), nullable=False)


class SanBayTrungGian(Base):
    san_bay_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey('chuyen_bay.id'), nullable=False)
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
        # db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10])
        #
        # db.session.commit()
        #
        # import hashlib
        #
        #
        # u = User(username='admin',
        #          password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)  # Use the ID of the created record
        # db.session.add(u)
        # db.session.commit()

        # info = ThongTinNguoiDung(ho_va_ten="admin", tai_khoan_id=u.id)
        # db.session.add(info)  # Add and commit information first
        # db.session.commit()

        # info2 = ThongTinNguoiDung(ho_va_ten="Nguyễn Xuân Lộc", so_dien_thoai='0362655091', dia_chi='Gia Lai', email='2151013052loc@gmail.com', CCCD='0798723983792')
        # db.session.add(info2)  # Add and commit information first
        # db.session.commit()