from datetime import datetime, timedelta
from flightapp.models import *
from flask_mail import Message
from flask import render_template

def add_minutes_to_time(time_str, minutes_to_add):
    # Chuyển đổi chuỗi thời gian thành đối tượng datetime
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    # Tạo một đối tượng timedelta để thêm số phút
    delta = timedelta(minutes=minutes_to_add)

    # Thêm số phút vào thời gian
    new_time = time_obj + delta

    # Trả về thời gian sau khi tính toán dưới dạng chuỗi
    return new_time.strftime('%H:%M:%S')
