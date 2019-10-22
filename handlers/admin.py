from flask import render_template, request


def main():
    # if there's no user with admin privileges yet in the Datastore, show the admin registration page (the first
    # user to register will automatically become the admin. After that the admin registration page will no longer
    # be available
    return render_template("admin/main.html")
