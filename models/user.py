from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class Session(ndb.Model):
    pass


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    username = ndb.StringProperty()
    password_hash = ndb.StringProperty()  # use bcrypt: http://zetcode.com/python/bcrypt/, rounds=12

    admin = ndb.BooleanProperty(default=False)
    suspended = ndb.BooleanProperty(default=False)
    session_tokens = ndb.StructuredProperty(Session, repeated=True)

    # standard model fields
    created = ndb.DateTimeProperty(auto_now_add=True)  # use https://github.com/miguelgrinberg/Flask-Moment
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)
