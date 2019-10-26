import os
from flask import Flask
from handlers import public, admin

app = Flask(__name__) 

# URL ROUTES:

# public
app.add_url_rule(rule="/", endpoint="public.index", view_func=public.index, methods=["GET", "POST"])
app.add_url_rule(rule="/login", endpoint="public.login", view_func=public.login, methods=["GET", "POST"])
app.add_url_rule(rule="/first-admin", endpoint="public.first_admin", view_func=public.first_admin_registration,
                 methods=["GET", "POST"])

# admin
app.add_url_rule(rule="/admin", endpoint="admin.main", view_func=admin.main, methods=["GET", "POST"])


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
