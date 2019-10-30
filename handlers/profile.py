from flask import request, render_template, redirect, url_for

from models.user import User
from utils.decorators import login_required


@login_required
def main(**params):
    if request.method == "GET":
        return render_template("profile/main.html", **params)


@login_required
def session_delete(**params):
    if request.method == "POST":
        token_hash_five_chars = request.form.get("delete-session-token")
        User.delete_session(user=params["user"], token_hash_five_chars=token_hash_five_chars)

        return redirect(url_for("profile.main"))
