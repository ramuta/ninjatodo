import functools
import logging

from flask import request, abort

from models.user import User


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning("BLA BLA BLA")
        logging.warning("{}".format(request.cookies.get("ninja-todo-session")))

        session_token = request.cookies.get("ninja-todo-session")

        if User.get_by_session_token(session_token=session_token):
            return func(*args, **kwargs)
        else:
            return abort(403)

    return wrapper


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning("BLA BLA BLA")
        logging.warning("{}".format(request.cookies.get("ninja-todo-session")))

        session_token = request.cookies.get("ninja-todo-session")

        user = User.get_by_session_token(session_token=session_token)

        if user.admin:
            return func(*args, **kwargs)
        else:
            return abort(403)

    return wrapper
