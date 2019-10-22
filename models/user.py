from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class Session(ndb.Model):
    pass


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email_address = ndb.StringProperty(repeated=True)  # user can have multiple email addresses
    admin = ndb.BooleanProperty(default=False)
    suspended = ndb.BooleanProperty(default=False)
    session_tokens = ndb.StructuredProperty(Session, repeated=True)

    # standard model fields
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)
