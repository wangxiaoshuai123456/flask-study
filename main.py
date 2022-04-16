from flask import Flask, redirect, url_for, request, render_template, make_response, session, escape, abort, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from forms import ContactForm

import sqlite3
import sqlite3 as sql

# conn = sqlite3.connect('database.db')
# print("Opened database successfully")
#
# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print("Table created successfully")
# conn.close()

app = Flask(__name__)
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_new')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['addr']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO students (name,addr,city,pin)\
                VALUES(?, ?, ?, ?)", (nm, addr, city, pin))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            return render_template('success.html')
    else:
        return render_template('contact.html', form=form)


# @app.route('/')
# def first_page():
#     return render_template('login_wsp.html')

app.config['UPLOAD_FOLDER'] = 'D:/study/flask-iptv/upload/'

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '1243998690@qq.com'
app.config['MAIL_PASSWORD'] = 'wqwhkdmfxsaagcgj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/idx")
def index():
    msg = Message('Hello', sender='1243998690@qq.com', recipients=['1243998690@qq.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        return 'file uploaded successfully'

    else:

        return render_template('upload.html')


@app.route('/login_wsp', methods=['GET', 'POST'])
def login_wsp():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['pwd'] == 'admin':
            return redirect(url_for('successOK'))
        else:
            return "用户名，密码错误，请重试 <br><a href = '/'></b>点击这里登录</b></a>"
    # abort(401)

    else:
        return redirect(url_for('first_page'))


@app.route('/successOK')
def successOK():
    return 'logged in successfully'


#
# # @app.route('/index')
# @app.route('/')
# def index():
#     return render_template('index.html')
#     # if 'username' in session:
#     #     username = session['username']
#     #
#     #     return '登录用户名是:' + username + '<br>' + \
#     #            "<b><a href = '/logout'>点击这里注销</a></b>"
#     #
#     # return "您暂未登录， <br><a href = '/login'></b>" + \
#     #        "点击这里登录</b></a>"


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         print('usename:', session['username'])
#
#         return redirect(url_for('index'))
#
#     return '''
#    <form action = "" method = "post">
#
#       <p><input type="text" name="username"/></p>
#
#       <p><input type="submit" value ="登录"/></p>
#
#    </form>
#
#    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there

    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/set_cookies')
def set_cookie():
    resp = make_response('set_cookie')
    resp.set_cookie('wsp', '123456789', max_age=120)
    return resp


@app.route('/get_cookies')
def get_cookie():
    cookie_value = request.cookies.get("wsp")
    print('cookie:', cookie_value)
    return cookie_value


@app.route('/del_cookies')
def del_cookie():
    resp = make_response('del_cookie')
    resp.delete_cookie('wsp')
    return resp


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == "POST":
        form_data = request.form
        return render_template('result.html', data=form_data)


@app.route('/mindex')
def mindex():
    return render_template('index.html')


@app.route('/hello')
def hello():
    my_int = 18
    my_str = 'curry'
    my_list = [1, 5, 4, 3, 2]
    my_dict = {
        'name': 'durant',
        'age': 28
    }

    return render_template('hello.html', my_int=my_int, my_str=my_str, my_list=my_list, my_dict=my_dict)


@app.route('/success/<name>')
def success(name):
    return 'You can success %s' % name


@app.route('/login', methods=['POST', 'GET'])
def hello_login():
    if request.method == "POST":
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


@app.route('/wsp')
def hello_wsp():
    return 'Hello wsp'


@app.route('/python/')
def hello_python():
    return 'Hello python'


@app.route('/hello/<name>')
def hello_world(name):
    return 'Hello %s' % name


@app.route('/hello/<int:age>')
def print_age(age):
    return 'age is %d' % age


@app.route('/hello/<float:score>')
def print_score(score):
    return 'score is %f' % score


@app.route('/user/<user>')
def print_user(user):
    if user == "admin":
        return redirect(url_for('hello_python'))
    else:
        return redirect(url_for('hello_world', name=user))


if __name__ == '__main__':
    app.run()
