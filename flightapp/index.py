from flask import Flask, render_template


app = Flask(__name__)


@app.route('/login')
def login():
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


if __name__ == '__main__':
    app.run(debug=True)