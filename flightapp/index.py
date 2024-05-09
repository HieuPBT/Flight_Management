from flask import Flask, render_template, request, redirect
from flightapp import app, login, dao
from flask_login import login_user, logout_user, login_required


@app.route('/')
def index():
    SB = dao.load_sanbay()
    HV = dao.load_hangve()
    return render_template('index.html', SB=SB, HV=HV)


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


@app.route('/register')
def register():
    return render_template('auth/register.html')


@app.route('/search_ticket')
def search_ticket():
    return render_template('ticket.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(int(user_id))


if __name__ == '__main__':
    with app.app_context():
        from flightapp import admin

        app.run(debug=True)
