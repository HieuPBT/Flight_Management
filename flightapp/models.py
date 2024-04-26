from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from flightapp import db, app
from flask_login import UserMixin
from enum import Enum as RoleEnum
from datetime import datetime


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class KhachHang(Base, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    ho_va_ten = Column(String(50), nullable=False)
    so_dien_thoai = Column(String(20))
    dia_chi = Column(String(255))
    email = Column(String(50))
    CCCD = Column(String(20))
    ve = relationship('Ve', backref='khach_hang', lazy=True)


class NhanVienQuanTri(KhachHang):
    chuyen_bay = relationship('ChuyenBay', backref='nhan_vien_quan_tri', lazy=True)


class NhanVienBanVe(KhachHang):
    ve = relationship('Ve', backref='nhan_vien_ban_ve', lazy=True)


class SanBay(Base):
    ten = Column(String(20), nullable=False)
    thanh_pho = Column(String(20), nullable=False)
    tuyen_bay_di = relationship('TuyenBay', foreign_keys='TuyenBay.san_bay_di_id', backref='san_bay', lazy=True)
    tuyen_bay_den = relationship('TuyenBay', foreign_keys='TuyenBay.san_bay_den_id', backref='san_bay', lazy=True)
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
    ngay_khoi_hanh = Column(DateTime, nullable=False)
    thoi_gian_bay = Column(Integer, nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey('tuyen_bay.id'), nullable=False)
    nhan_vien_quan_tri_id = Column(Integer, ForeignKey('nhan_vien_quan_tri.id'), nullable=False)
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
    khach_hang_id = Column(Integer, ForeignKey('khach_hang.id'), nullable=False)
    hoa_don_id = Column(Integer, ForeignKey('hoa_don.id'), nullable=False)
    nhan_vien_ban_ve_id = Column(Integer, ForeignKey('nhan_vien_ban_ve.id'), nullable=False)


class HoaDon(Base):
    ve_id = Column(Integer, ForeignKey('ve.id'), nullable=False)


class SanBayTrungGian(Base):
    san_bay_id = Column(Integer, ForeignKey('san_bay.id'), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey('chuyen_bay.id'), nullable=False)
    __table_args__ = (
        UniqueConstraint('san_bay_id', 'chuyen_bay_id'),
    )





if __name__ == '__main__':
    with app.app_context():
        db.create_all()