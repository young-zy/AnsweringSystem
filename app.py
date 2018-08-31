from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import escape

import json

app = Flask(__name__)
app.secret_key = "ADDQWEDFAFAEAED"

app.f = open("data.json", encoding="utf-8")
app.data = json.load(app.f)


@app.before_request
def process_request():
    if request.path == "/login":
        return None
    if not session.get("user_info"):
        return redirect("/login")
    return None


@app.route('/')
def index():
    if 'username' in session:
        return redirect('/answer/%d' % session.get("number"))
    return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get('username')
        session["username"] = username
        session["number"] = 1
        return redirect("/answer/1")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/login')


@app.route('/answer/<int:number>', methods=['GET', 'POST'])
def answer(number):
    if request.method == "GET":
        return render_template('answer.html', number=number)
    else:
        session['%d' % int(request.form.get('number'))] = request.form.get('group1')
        number = number + 1
        session['number'] = number
        return redirect('/answer/%d' % number)


if __name__ == '__main__':
    app.run(debug=True)
