import datetime
import functools

from flask import request, abort, url_for
from werkzeug.utils import redirect

from models.user import User


def public_handler(func):
    @functools.wraps(func)
    def wrapper(**params):
        session_token = request.cookies.get("ninja-todo-session")

        params["now"] = datetime.datetime.now()  # send current date to handler and HTML template

        if session_token:
            user = User.get_by_session_token(session_token=session_token)
            params["user"] = user

        return func(**params)

    return wrapper


def login_required(func):
    @functools.wraps(func)
    def wrapper(**params):
        session_token = request.cookies.get("ninja-todo-session")

        params["now"] = datetime.datetime.now()  # send current date to handler and HTML template

        if session_token:
            user = User.get_by_session_token(session_token=session_token)
            params["user"] = user

            if user:
                return func(**params)

        return redirect(url_for("public.login"))

    return wrapper


def admin_required(func):
    @functools.wraps(func)
    def wrapper(**params):
        session_token = request.cookies.get("ninja-todo-session")

        params["now"] = datetime.datetime.now()  # send current date to handler and HTML template

        if session_token:
            user = User.get_by_session_token(session_token=session_token)
            params["user"] = user

            if user and user.admin:
                return func(**params)
            elif user:
                return abort(403)

        return redirect(url_for("public.login"))

    return wrapper
