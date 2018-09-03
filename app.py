from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import g

import json

app = Flask(__name__)
app.secret_key = "dashfbdkfbasdkfvnmasdfnc"


@app.before_request
def before_request():
    assert isinstance(g, object)
    g.f = open("data.json", encoding="utf-8")
    g.data = json.load(g.f)
    g.dict_arr = g.data['list']
    g.total_num = len(g.dict_arr)
    g.id_list = []
    for i in range(1, g.total_num+1):
        g.id_list.append(i)

    if request.path == "/login":
        return None
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
        session["total_num"] = g.total_num
        return redirect('/answer/1')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('number', None)
    return redirect('/login')


@app.route('/answer/<int:number>', methods=['GET', 'POST'])
def answer(number):
    if request.method == "GET":
        if 'username' in session:
            return render_template('answer.html', number=number, total_num=g.total_num,
                                   id_list=g.id_list, question=g.dict_arr[number-1]["title"],
                                   img_path=g.dict_arr[number-1]["imgpath"],
                                   item=g.dict_arr[number-1]["items"])
        else:
            return redirect('/login')
    else:
        tmp = request.form.get('group1')
        if tmp is not None:
            session['%d' % int(request.form.get('number'))] = tmp
            number = number + 1
        else:
            if number is not 1:
                number = number - 1
        session['number'] = number
        return redirect('/answer/%d' % number)


if __name__ == '__main__':
    app.run(debug=True)
