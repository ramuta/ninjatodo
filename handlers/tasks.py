from flask import request, render_template

from utils.decorators import login_required


@login_required
def my_tasks():
    if request.method == "GET":
        return render_template("tasks/my-tasks.html")
