from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from flightapp import db, app
from flask_login import UserMixin
from enum import Enum as enum
from datetime import datetime


class UserRole(enum):
    USER = 1
    ADMIN = 2
    TICKET_SELLER = 3


class QuyDinhKey(enum):
    NUAIRPORT = "Số lượng sân bay"
    MINFLIGHT = "Thời gian bay tối thiểu"
    MAXIMAIRPORT = "Số lượng sân bay trung gian tối đa"
    MINSTOP = "Thời gian đừng tối thiểu"
    MAXSTOP = "Thời gian dừng tối đa"
    NUTICKETCLASS = "Số lượng hạng vé"
    BASEPRICE = "Đơn giá vé"
    SOLDTIME = "Thời gian bán vé"
    BOOKINGTIME = "Thời gian đặt vé"

    def __str__(self):
        return self.name


class Cot(enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'


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
    cot = Column(Enum(Cot), nullable=False)
    hang = Column(Integer, nullable=False)
    ghe_may_bay = relationship('GheMayBay', backref='ghe', lazy=True)

    __table_args__ = (
        UniqueConstraint('cot', 'hang'),
    )


class MayBay(Base):
    ten = Column(String(20), nullable=False)
    ghe_may_bay = relationship('GheMayBay', backref='may_bay', lazy=True)
    # chuyen_bay = relationship('ChuyenBay', backref='may_bay', lazy=True)

    def __str__(self):
        return self.ten


class HangVe(Base):
    ten = Column(String(20), nullable=False)
    hang_ve_chuyen_bay = relationship('HangVeChuyenBay', backref='hang_ve', lazy=True)
    ghe_may_bay = relationship('GheMayBay', backref='hang_ve', lazy=True)

    def __str__(self):
        return self.ten


class ChuyenBay(Base):
    ngay_gio_khoi_hanh = Column(DateTime, nullable=True)
    thoi_gian_bay = Column(Integer, nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey('tuyen_bay.id'), nullable=False)
    tuyen_bay = relationship('TuyenBay', foreign_keys=[tuyen_bay_id], lazy=True)
    nhan_vien_quan_tri_id = Column(Integer, ForeignKey('user.id'), nullable=True)
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
    hang_ve_id = Column(Integer, ForeignKey('hang_ve.id'), nullable=False)
    __table_args__ = (
        UniqueConstraint('ghe_id', 'may_bay_id'),
    )


class Ve(Base):
    ghe_may_bay_id = Column(Integer, ForeignKey('ghe_may_bay.id'), nullable=False)
    hang_ve_chuyen_bay_id = Column(Integer, ForeignKey('hang_ve_chuyen_bay.id'), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey('thong_tin_nguoi_dung.id'), nullable=False)
    hoa_don_id = Column(Integer, ForeignKey('hoa_don.id'), nullable=True)
    __table_args__ = (
        UniqueConstraint('ghe_may_bay_id', 'hang_ve_chuyen_bay_id'),
    )


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
    key = Column(Enum(QuyDinhKey), nullable=False, unique=True)
    value = Column(Integer, nullable=False)
    nhan_vien_quan_tri_id = Column(Integer, ForeignKey('user.id'), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
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
        # u2 = User(username='admin2',
        #          password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)  # Use the ID of the created record
        # db.session.add(u2)
        # db.session.commit()
        #
        # info3 = ThongTinNguoiDung(ho_va_ten="admin2", tai_khoan_id=2)
        # db.session.add_all([info3])  # Add and commit information first
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
        # tb2 = TuyenBay(san_bay_di_id=6, san_bay_den_id=5)  # HN - HCM
        # tb3 = TuyenBay(san_bay_di_id=1, san_bay_den_id=2)  # Cà Mau - Cần Thơ
        # tb4 = TuyenBay(san_bay_di_id=9, san_bay_den_id=10)  # Hue - Nghệ An
        # db.session.add_all([tb1, tb2, tb3, tb4])
        #
        # db.session.commit()
        #
        # # Tạo danh sách ghế và máy bay
        # mb1 = MayBay(ten='BOE701')
        # mb2 = MayBay(ten='VietAir234')
        # mb3 = MayBay(ten='AirJet709')
        # danh_sach_ghe = []
        # danh_sach_may_bay = [mb1, mb2, mb3]
        #
        # # Số hàng và số cột
        # so_hang = 50
        # so_cot = ['A', 'B', 'C', 'D', 'E', 'F']
        #
        # # Tạo 300 ghế
        # for hang in range(1, so_hang + 1):
        #     for cot in so_cot:
        #         ghe = Ghe(cot=Cot[cot], hang=hang)
        #         danh_sach_ghe.append(ghe)
        #
        # # Lưu trữ ghế vào cơ sở dữ liệu
        # db.session.add_all(danh_sach_ghe)
        # db.session.add_all(danh_sach_may_bay)
        # db.session.commit()
        #
        # hv1 = HangVe(ten='Thương Gia')
        # hv2 = HangVe(ten='Phổ Thông')
        # hv3 = HangVe(ten='Tiết Kiệm')
        #
        # db.session.add_all([hv3, hv1, hv2])
        #
        # db.session.commit()
        # # Thiết lập mối quan hệ giữa ghế và máy bay
        # for i in danh_sach_may_bay:
        #     for j in danh_sach_ghe:
        #         if j.hang < 3:
        #             ghe_may_bay = GheMayBay(ghe_id=j.id, may_bay_id=i.id, hang_ve_id=hv1.id)
        #             db.session.add(ghe_may_bay)
        #         else:
        #             ghe_may_bay = GheMayBay(ghe_id=j.id, may_bay_id=i.id, hang_ve_id=hv2.id)
        #             db.session.add(ghe_may_bay)
        #
        # db.session.commit()
        #
        #
        # qd1 = QuyDinh(key=QuyDinhKey.NUAIRPORT, value=10, nhan_vien_quan_tri_id=1)
        # qd2 = QuyDinh(key=QuyDinhKey.MINFLIGHT, value=30, nhan_vien_quan_tri_id=1)
        # qd3 = QuyDinh(key=QuyDinhKey.MAXIMAIRPORT, value=3, nhan_vien_quan_tri_id=1)
        # qd4 = QuyDinh(key=QuyDinhKey.MAXSTOP, value=30, nhan_vien_quan_tri_id=1)
        # qd5 = QuyDinh(key=QuyDinhKey.MINSTOP, value=15, nhan_vien_quan_tri_id=1)
        # qd6 = QuyDinh(key=QuyDinhKey.BASEPRICE, value=300000, nhan_vien_quan_tri_id=1)
        # qd7 = QuyDinh(key=QuyDinhKey.BOOKINGTIME, value=720, nhan_vien_quan_tri_id=1)
        # qd8 = QuyDinh(key=QuyDinhKey.SOLDTIME, value=240, nhan_vien_quan_tri_id=1)
        # qd9 = QuyDinh(key=QuyDinhKey.NUTICKETCLASS, value=3, nhan_vien_quan_tri_id=1)
        #
        # db.session.add_all([qd1, qd2, qd3, qd4, qd5, qd6, qd7, qd8, qd9])
        #
        # db.session.commit()
