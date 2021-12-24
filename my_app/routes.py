from my_app.common import *
from my_app.models import *
from my_app import login_manager
from flask_login import login_user, logout_user, login_required, current_user
from my_app import admin, manage
from my_app import utils


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/user/databases/detail/<string:name>", methods=["POST", "GET"])
def detail():
    render_template("/admin/detail-database.html")


@login_manager.user_loader
def user_load(user_id):
    return Users.query.get(user_id)


@app.route("/login", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def login_account():
    if request.method == 'POST':
        getEmail = request.form.get('email')
        getPassword = request.form.get('password')
        user = Users.query.filter_by(Email=getEmail, IsDelete = 0).first()
        if user and user.Password == getPassword:
            if user.IsAdmin == 0:
                if user.Active == 1:
                    login_user(user)
                    session.permanent = True
                    return redirect(url_for('_user.index'))
                else:
                    flash('Tài khoản bị khóa! Vui lòng liên hệ đến quản trị viên')
                    return render_template("login.html")
            else:
                login_user(user)
                session.permanent = True
                return redirect(url_for('_manage.index'))
        else:
            flash('Tên người dùng hoặc mật khẩu không đúng! Vui lòng thử lại')
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    return render_template("register.html")


@app.route("/register/user", methods=["POST"])
def register_user():
    getEmail = request.form.get('email')
    getUserName = request.form.get('username')
    getPassword = request.form.get('password')
    getConfirmPassword = request.form.get('confirm_password')

    if getPassword == getConfirmPassword:
        checkEmail = Users.query.filter_by(Email=getEmail).first()
        if checkEmail:
            return redirect(url_for('register'))

        checkUserName = Users.query.filter_by(UserName=getUserName).first()
        if checkUserName:
            return redirect(url_for('register'))

        utils.add_user(getEmail, getUserName, getPassword)
    return redirect(url_for('login_account'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_account'))

