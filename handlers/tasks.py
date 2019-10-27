from flask import request, render_template


def my_tasks():
    if request.method == "GET":
        return render_template("tasks/my-tasks.html")
