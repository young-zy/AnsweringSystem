from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import g

import json

app = Flask(__name__)
app.secret_key = "dashfbdkfbasdkfvnmasdfnc"      """Please be sure to change this value 
                                                    into a long random value 
                                                    in the production environment
                                                    
                                                    Be sure that no one else can get this key,
                                                    since it encrypts the user session
                                                    """


@app.before_request
def before_request():
    assert isinstance(g, object)
    g.f = open("data.json", encoding="utf-8")
    g.data = json.load(g.f)
    g.f.close()
    g.dict_arr = g.data['list']
    g.total_num = len(g.dict_arr)
    g.id_list = []
    for i in range(1, g.total_num + 1):
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
        if 'username' in session:
            return redirect('/answer/%d' % session.get("number"))
        return render_template("login.html")
    else:
        username = request.form.get('username')
        session["username"] = username
        session["number"] = 1
        session["total_num"] = g.total_num
        return redirect('/answer/1')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/answer/<int:number>', methods=['GET', 'POST'])
def answer(number):
    if request.method == "GET":
        if 'username' in session:
            if 0 < number < g.total_num + 1:
                args = {}
                args.update(
                    number=number,
                    total_num=g.total_num,
                    id_list=g.id_list,
                    img_path=g.dict_arr[number - 1]["imgpath"],
                    question=g.dict_arr[number - 1]["title"],
                    item=g.dict_arr[number - 1]["items"],
                    selected=[]
                )
                if "%d" % number in session:
                    print(session.get("%d" % number))
                    args.update(selected=list(map(int, session.get("%d" % number))))
                if g.dict_arr[number - 1]["type"] == "multiple":
                    return render_template("answer-multiple.html", args=args)
                if g.dict_arr[number - 1]["type"] == "textfield":
                    return render_template("answer-textfield.html",args=args)
                return render_template('answer.html', args=args)
            else:
                return redirect("/login")
        else:
            return redirect('/login')
    else:
        if request.form.get("forward") == "true":
            if request.form.get("group1") is not None:
                session['%d' % int(request.form.get('number'))] = request.form.get("group1")
            else:
                session['%d' % int(request.form.get('number'))] = request.form.get("group2")
            number = number + 1
        else:
            if request.form.get('group1') is not None:
                session['%d' % int(request.form.get('number'))] = request.form.get('group1')
            number = number - 1
        session['number'] = number
        return redirect('/answer/%d' % number)


@app.route('/answer/submit', methods=['POST'])
def submit():
    if request.form.get("group1") is not None:
        session["%d" % g.total_num] = request.form.get("group1")
    else:
        session["%d" % g.total_num] = request.form.get("group2")
    g.answer_set = {"name": session.get("username")}
    try:
        g.f = open("answers/%s" % session.get("username"), "w")
        g.f.write("name: %s" % session.get("username") + "\n")
        for i in range(1, g.total_num + 1):
            if session.get("%d" % i) is not None:
                if g.dict_arr[i-1]["type"] == "textfield":
                    g.answer_set["%d" % i] = session.get("%d" % i)
                    g.f.write("%d. " % i)
                    g.f.write(session.get("%d" % i))
                else:
                    g.answer_set["%d" % i] = list(map(int, session.get("%d" % i)))
                    g.f.write("%d. " % i)
                    for item in list(map(int, session.get("%d" % i))):
                        g.f.write(case(item) + ", ")
                g.f.write("\n")
        g.f.write(str(g.answer_set))
    finally:
        g.f.close()
        g.answer_set.clear()
    return redirect("/logout")


def case(i):
    if i == 0:
        return "A"
    elif i == 1:
        return "B"
    elif i == 2:
        return "C"
    elif i == 3:
        return "D"
    else:
        return "ERROR"


if __name__ == '__main__':
    app.run(debug=True)
