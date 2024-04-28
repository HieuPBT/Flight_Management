from flask import Flask, render_template
from flightapp import app, login


@app.route('/login')
def login_user():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/search_ticket')
def search_ticket():
    return render_template('ticket.html')


@app.route('/')
def home():
    return render_template('index.html')


@login.user_loader
def load_user(user_id):
    pass


if __name__ == '__main__':
    with app.app_context():
        from flightapp import admin
        app.run(debug=True)
