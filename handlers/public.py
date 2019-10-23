from flask import render_template, request, redirect, url_for

from models.user import User


def index():
    return render_template("public/index.html")


def login():
    return render_template("public/login.html")


def first_admin_registration():
    # this handler is needed only to set the first user/admin of the web app, so that the user can invite others
    # to the app (there's no registration system because the app is not open to just anyone).

    # find a user with admin privileges - if such user exists, redirect to index
    if User.is_there_any_admin():
        return redirect(url_for("public.index"))

    # if such user does not exist, enable the option to set the first admin via first-admin-register.html
    if request.method == "GET":
        return render_template("public/first-admin-register.html")
    elif request.method == "POST":
        username = request.form.get("first-admin-username")
        password = request.form.get("first-admin-password")
        repeat = request.form.get("first-admin-repeat")

        if username and password and password == repeat:
            user = User.create(username=username, password=password, admin=True)

            return render_template("public/first-admin-success.html")
