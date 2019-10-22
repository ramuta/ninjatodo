from flask import render_template, request


def index():
    return render_template("public/index.html")


def login():
    return render_template("public/login.html")
