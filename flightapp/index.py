from flask import Flask, render_template, request, redirect, jsonify, url_for, session, signals
from flightapp import app, login, dao, configs, mail
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from flightapp.decorators import loggedin
from models import *
import json
import uuid
import requests
import hmac
import hashlib
import random
from time import time
from datetime import datetime


@app.route('/')
def index():
    SB = dao.load_airport()
    HV = dao.load_ticket_class()
    to_day = datetime.now().date()
    msg = Message(subject="Trang Chu", sender=('test', '2151013204hieu@ou.edu.vn'), recipients=['2151013052loc@gmail.com'])
    msg.body = "Dat ve Online"
    mail.send(msg)
    return render_template('index.html', SB=SB, HV=HV, to_day=to_day)


@app.route('/api/create_flight_schedule', methods=['POST'])
def create_flight_schedule():
    if request.method.__eq__('POST'):
        depart = request.form.get('depart')
        plane = request.form.get('plane')
        depart_date_time = request.form.get('depart_date_time')
        flight_duration = request.form.get('flight_duration')
        tickets_data = json.loads(request.form.get('tickets_data'))
        im_airport = json.loads(request.form.get('im_airport'))
        print(tickets_data)
        print(im_airport)

        try:
            dao.add_flight_schedule(depart, depart_date_time, flight_duration, plane, tickets_data, im_airport)
        except Exception as ex:
            print(ex)
            return redirect('/admin/chuyenbay/')
        else:
            return redirect('/admin/chuyenbay/')

    # return jsonify({'depart': depart,
    #                 'depart_date_time': depart_date_time,
    #                 'flight_duration':flight_duration,
    #                 'tickets_data': tickets_data,
    #                 'plane': plane,
    #                 'im_airport': im_airport})


@app.route('/api/search_flight')
def search_flight(hv_id, ):
    pass


@app.route('/login-admin', methods=['POST'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)

    if u:
        login_user(user=u)

    return redirect('/admin')


@loggedin
@app.route('/register', methods=['POST', 'GET'])
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            dao.add_user(name=request.form.get('name'),
                         username=request.form.get('username'),
                         password=password,
                         email=request.form.get('email'),
                         cccd=request.form.get('cccd'),
                         phone_number=request.form.get('phone_number'),
                         address=request.form.get('address'))

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('auth/register.html', err_msg=err_msg)


@loggedin
@app.route('/login', methods=['get', 'post'])
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = 'Username hoặc password không đúng!'

    return render_template('auth/login.html', err_msg=err_msg)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/search_flights', methods=['POST'])
def search_flights():
    passengers = request.form.get('passengers')
    ticket_class = request.form.get('ticket_class')
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    leave_date = request.form.get('leave_date')
    chuyen_bay_list = dao.get_available_flights(departure, destination, ticket_class, passengers, leave_date)
    return render_template("flight_results.html", chuyen_bay_list=chuyen_bay_list, passengers_quantity=passengers)


@app.route('/tickets_info')
def tickets_info():
    passengers_quantity = request.args.get('passengers_quantity')
    hang_ve_chuyen_bay_id = request.args.get('hang_ve_chuyen_bay_id')
    price = request.args.get('total_price')
    passengers_quantity = int(passengers_quantity)
    hang_ve_chuyen_bay_id = int(hang_ve_chuyen_bay_id)
    available_seats = dao.get_available_seats(hang_ve_chuyen_bay_id)
    return render_template('tickets_info.html', hang_ve_chuyen_bay_id=hang_ve_chuyen_bay_id,
                           passengers_quantity=passengers_quantity, available_seats=available_seats,
                           total_price=int(price) * passengers_quantity)


@app.route('/add_tickets_info', methods=['POST'])
def add_tickets_info():
    string_numbers = request.form['selected_seats']
    selected_seats = string_numbers.split(",")

    # Chuyển đổi các phần tử từ chuỗi sang số nguyên
    numbers = list(map(int, selected_seats))
    for i in range(int(request.form['passengers_quantity'])):
        seat = dao.get_seat_plane(numbers[i], int(request.form['hang_ve_chuyen_bay_id']))
        u = dao.add_user_info(request.form[f'name_{i}'], request.form[f'phoneNumber_{i}'], request.form[f'address_{i}'],
                              request.form[f'cccd_{i}'], request.form[f'email_{i}'])
        dao.add_ticket(seat.id, int(request.form['hang_ve_chuyen_bay_id']), u.id)

    return jsonify({'ok': '200'})


@app.route('/admin/update_stats', methods=['POST'])
def update_stats():
    month = request.json['month']
    year = request.json['year']
    revenue_by_route = dao.stats_route_revenue(year, month)
    total = 0
    for i in revenue_by_route:
        total += i[2]
    return jsonify({"revenue_by_route": revenue_by_route, "total": total})


@app.route('/api/momo-pay', methods=['POST'])
def momo_pay():
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    requestId = str(uuid.uuid4())
    amount = str((request.json.get('total')))
    print(amount)
    orderId = str(uuid.uuid4())
    # orderId = total.get('appointment_id')+total.get('user_id')+total.get('booking_date')
    orderInfo = "pay with MoMo"
    requestType = "captureWallet"
    extraData = ""
    redirectUrl = "https://6757-171-243-48-141.ngrok-free.app/"
    ipnUrl = "https://6757-171-243-48-141.ngrok-free.app/api/momo-pay/ipn"
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Vé Máy Bay Giá Rẻ",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }

    data = json.dumps(data)

    clen = len(data)
    response = requests.post(endpoint, data=data,
                             headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    if response.status_code == 200:
        data1 = request.json
        print(data1)
        response_data = response.json()
        # string_numbers = session.get('selected_seats')
        # print(string_numbers)
        # dao.add_tickets_info(orderId, partnerCode)

        print(response.json())
        return jsonify({'ok': '200',
                        'payUrl': response_data.get('payUrl')})
        # return redirect(response_data.get('payUrl'))

    else:
        print(response.json())
        return jsonify({'error': 'Invalid request method'})


@app.route('/api/momo-pay/ipn', methods=['POST'])
def momo_ipn():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    result_code = data["resultCode"]
    orderId = data['orderId']

    if result_code != 0:
        return jsonify({'error': "Thanh toán thất bại",
                        'status': 400})

    try:
        dao.update_bill(orderId)
        return jsonify({'status': 200})
    except Exception as e:
        return jsonify({'status': 500, 'error': str(e)})


@app.route('/api/zalo-pay', methods=['POST'])
def zalo_pay():
    endpoint = "https://sb-openapi.zalopay.vn/v2/create"
    appid = 2553
    key1 = "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL"
    appuser = "user123"
    transID = random.randrange(1000000)
    apptime = int(round(time() * 1000))  # miliseconds
    app_trans_id = "{:%y%m%d}_{}".format(datetime.today(), transID)
    embeddata = json.dumps({"redirecturl": "https://546f-171-243-48-141.ngrok-free.app/"})
    item = json.dumps([{}])
    amount = 400000
    callback_url = "https://546f-171-243-48-141.ngrok-free.app/api/zalo-pay/callback"

    # Tạo chuỗi dữ liệu theo định dạng yêu cầu
    raw_data = "{}|{}|{}|{}|{}|{}|{}".format(appid, app_trans_id, appuser, amount, apptime, embeddata, item)

    # Tính toán MAC bằng cách sử dụng HMAC
    mac = hmac.new(key1.encode(), raw_data.encode(), hashlib.sha256).hexdigest()

    # Dữ liệu gửi đi
    data = {
        "app_id": appid,
        "app_user": appuser,
        "app_time": apptime,
        "amount": amount,
        "app_trans_id": app_trans_id,
        "embed_data": embeddata,
        "item": item,
        "description": "Lazada - Payment for the order #" + str(transID),
        "bank_code": "zalopayapp",
        "mac": mac,
        "callback_url": callback_url
    }

    # Gửi yêu cầu tạo
    response = requests.post(url=endpoint, data=data)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
        return jsonify({'ok': '200', 'order_url': response_data.get('order_url')})
    else:
        return jsonify({'error': 'Invalid request method'}), 400


@app.route('/api/zalo-pay/callback', methods=['POST'])
def callback():
    result = {}
    key2 = "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz"
    try:
        cbdata = request.json
        mac = hmac.new(key2.encode(), cbdata['data'].encode(), hashlib.sha256).hexdigest()

        # kiểm tra callback hợp lệ (đến từ ZaloPay server)
        if mac != cbdata['mac']:
            # callback không hợp lệ
            result['returncode'] = -1
            result['returnmessage'] = 'mac not equal'
        else:
            # thanh toán thành công
            # merchant cập nhật trạng thái cho đơn hàng
            dataJson = json.loads(cbdata['data'])
            print("update order's status = success where apptransid = " + dataJson['apptransid'])

            result['returncode'] = 1
            result['returnmessage'] = 'success'
    except Exception as e:
        result['returncode'] = 0  # ZaloPay server sẽ callback lại (tối đa 3 lần)
        result['returnmessage'] = str(e)

    # thông báo kết quả cho ZaloPay server
    print(result)
    return jsonify(result)


@app.context_processor
def common_attributes():
    return {
        'ticketclass': dao.load_ticket_class(),
        'plane': dao.load_plane(),
        'airport': dao.load_airport(),
        'flight_route': dao.load_flight_route(),
        'maxinairport': dao.load_config(QuyDinhKey.MAXIMAIRPORT).value,
        'minstop': dao.load_config(QuyDinhKey.MINSTOP).value,
        'nuticketclass': dao.load_config(QuyDinhKey.NUTICKETCLASS).value,
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(int(user_id))


if __name__ == '__main__':
    with app.app_context():
        from flightapp import admin

        app.run(debug=True)
