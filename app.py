import os

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from database import User
from database import UserInterest


app = Flask(__name__)


@app.route("/")
def index():
    users = User.select()
    return render_template("index.html", users=users)


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
    user = User.create(
        line_id=line_id, prefecture=prefecture, municipality=municipality
    )
    user_interest = UserInterest.create(
        user_id=user.id,
        category01=category01,
        category02=category02,
        category03=category03,
    )
    return redirect("/")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
