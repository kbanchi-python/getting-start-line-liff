import os

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from database import User
from database import LineUser
from database import LineUserInterest


app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(id=int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/")
def index():
    users = LineUser.select()
    return render_template("index.html", users=users)


@app.route("/signup", methods=["GET"])
def signupGet():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signupPost():
    name = request.form.get("name")
    password = request.form.get("password")
    generate_password = generate_password_hash(password, method="sha256")
    User.create(name=name, password=generate_password)
    return redirect("/login")


@app.route("/login", methods=["GET"])
def loginGet():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginPost():
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.get(name=name)
    if check_password_hash(user.password, password):
        login_user(user)
        return redirect("/")
    generate_password = generate_password_hash(password, method="sha256")
    User.create(name=name, password=generate_password)
    return redirect("/login")


@app.route("/setting")
def setting():
    prefecture = request.args.get("prefecture")
    municipality = request.args.get("municipality")
    if not prefecture or not municipality:
        return redirect("/")
    return render_template(
        "setting.html", prefecture=prefecture, municipality=municipality
    )


@app.route("/setting", methods=["POST"])
def setting_post():
    line_id = request.form["line_id"]
    prefecture = request.form["prefecture"]
    municipality = request.form["municipality"]
    category01 = request.form.get("category01")
    category02 = request.form.get("category02")
    category03 = request.form.get("category03")
    if not prefecture or not municipality:
        return redirect("/")
    line_user = LineUser.create(
        line_id=line_id, prefecture=prefecture, municipality=municipality
    )
    line_user_interest = LineUserInterest.create(
        user_id=line_user.id,
        category01=category01,
        category02=category02,
        category03=category03,
    )
    return redirect("/")


@app.route("/delivery")
def delivery():
    return render_template("delivery.html")


@app.route("/delivery", methods=["POST"])
def delivery_post():
    return redirect("/delivery")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
