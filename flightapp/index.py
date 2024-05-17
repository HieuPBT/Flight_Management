from flask import Flask, render_template, request, redirect, jsonify, url_for
from flightapp import app, login, dao, configs
from flask_login import login_user, logout_user, login_required

from flightapp.decorators import loggedin
from models import *
import json


@app.route('/')
def index():
    SB = dao.load_airport()
    HV = dao.load_ticket_class()
    to_day = datetime.now().date()
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
            return jsonify({'status': 500})
        else:
            return jsonify({'status': 200})

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
    price = request.args.get('price')
    print(price)
    passengers_quantity = int(passengers_quantity)
    hang_ve_chuyen_bay_id = int(hang_ve_chuyen_bay_id)
    available_seats = dao.get_available_seats(hang_ve_chuyen_bay_id)
    return render_template('tickets_info.html', hang_ve_chuyen_bay_id=hang_ve_chuyen_bay_id, passengers_quantity=passengers_quantity, available_seats=available_seats, total_price=int(price)*passengers_quantity)


@app.route('/add_tickets_info', methods=['POST'])
def add_tickets_info():
    string_numbers = request.form['selected_seats']
    selected_seats = string_numbers.split(",")

    # Chuyển đổi các phần tử từ chuỗi sang số nguyên
    numbers = list(map(int, selected_seats))
    for i in range(int(request.form['passengers_quantity'])):
        seat = dao.get_seat_plane(numbers[i], int(request.form['hang_ve_chuyen_bay_id'] ))
        u = dao.add_user_info(request.form[f'name_{i}'], request.form[f'phoneNumber_{i}'], request.form[f'address_{i}'], request.form[f'cccd_{i}'], request.form[f'email_{i}'])
        dao.add_ticket(seat.id, int(request.form['hang_ve_chuyen_bay_id']), u.id)

    return jsonify({'ok':'200'})


@app.route('/admin/update_stats', methods=['POST'])
def update_stats():
    month = request.json['month']
    year = request.json['year']
    revenue_by_route = dao.stats_route_revenue(year, month)
    total = 0
    for i in revenue_by_route:
        total += i[2]
    return jsonify({"revenue_by_route":revenue_by_route, "total":total})


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
