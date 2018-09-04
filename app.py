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
    session.clear()
    return redirect('/login')


@app.route('/answer/<int:number>', methods=['GET', 'POST'])
def answer(number):
    if request.method == "GET":
        if 'username' in session:
            if "%d" % number in session:
                if 0 < number < g.total_num:
                    return render_template('answer.html', number=number, total_num=g.total_num,
                                           id_list=g.id_list, question=g.dict_arr[number-1]["title"],
                                           img_path=g.dict_arr[number-1]["imgpath"],
                                           item=g.dict_arr[number-1]["items"],
                                           selected=int(session.get("%d" % number))
                                           )
                elif number == g.total_num + 1:
                    print(g.total_num + 1)
                    g.name = session.get("name")
                    g.answer_set = {"name": session.get("name")}
                    for i in range(1, g.total_num+1):
                        g.answer_set["%d" % i] = case(session.get("%d" % i))
                    try:
                        g.f = open("%s" % session.get("name"), )
                        g.f.write(str(g.answer_set))
                    finally:
                        g.f.close()
                    return redirect("/logout")
                else:
                    return redirect("/login")
            else:
                if 0 < number < g.total_num + 1:
                    return render_template('answer.html', number=number, total_num=g.total_num,
                                           id_list=g.id_list, question=g.dict_arr[number-1]["title"],
                                           img_path=g.dict_arr[number-1]["imgpath"],
                                           item=g.dict_arr[number-1]["items"]
                                           )
                elif number == g.total_num + 1:
                    try:
                        g.f = open("%s" % session.get("username"), "w")
                        g.name = session.get("name")
                        g.answer_set = {"name": session.get("username")}
                        g.f.write("name: %s" % session.get("username") + "\n")
                        for i in range(1, g.total_num+1):
                            if session.get("%d" % i) is not None:
                                g.answer_set["%d" % i] = case(int(session.get("%d" % i)))
                                g.f.write("%d. " % i + case(int(session.get("%d" % i))) + "\n")
                    finally:
                        g.f.write(str(g.answer_set))
                        g.f.close()
                        g.answer_set.clear()
                    return redirect("/logout")
                else:
                    return redirect("/login")
        else:
            return redirect('/login')
    else:
        if request.form.get("forward") == "true":
            session['%d' % int(request.form.get('number'))] = request.form.get('group1')
            number = number + 1
        else:
            number = number - 1
        session['number'] = number
        return redirect('/answer/%d' % number)


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
