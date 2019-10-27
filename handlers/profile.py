from flask import request, render_template

from utils.decorators import login_required


@login_required
def main(**params):
    if request.method == "GET":
        return render_template("profile/main.html", **params)
