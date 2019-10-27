import os

from flask import render_template, request, redirect, url_for, abort, make_response

from models.user import User
from utils.decorators import public_handler


@public_handler
def index(**params):
    return render_template("public/index.html", **params)


@public_handler
def login(**params):
    if request.method == "GET":
        return render_template("public/login.html", **params)

    elif request.method == "POST":
        username = request.form.get("login-username")
        password = request.form.get("login-password")

        if username and password:
            # find a User with this username (if it doesn't exist: 404)
            user = User.get_by_username(username=username)

            if not user:
                return abort(404)

            # check if passwords match (if not: 403)
            if User.is_password_valid(user=user, password=password):
                # if passwords match, generate a session token and save its hash in the database
                session_token = User.generate_session_token(user=user, request=request)

                # prepare a response and then store the token in a cookie
                response = make_response(redirect(url_for("tasks.my_tasks")))

                # on localhost don't make the cookie secure and http-only (but on production it should be)
                cookie_secure_httponly = False
                if os.getenv('GAE_ENV', '').startswith('standard'):
                    cookie_secure_httponly = True

                # store the token in a cookie
                response.set_cookie(key="ninja-todo-session", value=session_token, secure=cookie_secure_httponly,
                                    httponly=cookie_secure_httponly)
                return response

        return abort(403)


@public_handler
def first_admin_registration(**params):
    # this handler is needed only to set the first user/admin of the web app, so that the user can invite others
    # to the app (there's no registration system because the app is not open to just anyone).

    # find a user with admin privileges - if such user exists, redirect to index
    if User.is_there_any_admin():
        return redirect(url_for("public.index"))

    # if such user does not exist, enable the option to set the first admin via first-admin-register.html
    if request.method == "GET":
        return render_template("public/first-admin-register.html", **params)

    elif request.method == "POST":
        username = request.form.get("first-admin-username")
        password = request.form.get("first-admin-password")
        repeat = request.form.get("first-admin-repeat")

        if username and password and password == repeat:
            user = User.create(username=username, password=password, admin=True)

            return render_template("public/first-admin-success.html", **params)
