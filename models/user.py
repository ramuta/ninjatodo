import datetime
import secrets

import bcrypt

from google.cloud import ndb
from models.db_settings import get_db

client = get_db()


class Session(ndb.Model):
    token_hash = ndb.StringProperty()
    ip = ndb.StringProperty()
    platform = ndb.StringProperty()
    browser = ndb.StringProperty()
    user_agent = ndb.StringProperty()
    expired = ndb.DateTimeProperty()


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    username = ndb.StringProperty()
    password_hash = ndb.StringProperty()  # use bcrypt: http://zetcode.com/python/bcrypt/, rounds=12

    admin = ndb.BooleanProperty(default=False)
    suspended = ndb.BooleanProperty(default=False)
    sessions = ndb.StructuredProperty(Session, repeated=True)

    # standard model fields
    created = ndb.DateTimeProperty(auto_now_add=True)  # use https://github.com/miguelgrinberg/Flask-Moment
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, username, password, admin=False):
        with client.context():
            user = cls.query(cls.username == username).get()  # check if there's any user with the same name already

            if not user:
                # use bcrypt to hash the password
                hashed = bcrypt.hashpw(password=str.encode(password), salt=bcrypt.gensalt(12))

                # create the user object and store it into Datastore
                user = cls(username=username, password_hash=hashed, admin=admin)
                user.put()

            return user

    @classmethod
    def get_by_username(cls, username):
        with client.context():
            user = cls.query(cls.username == username).get()
            return user

    @classmethod
    def is_password_valid(cls, user, password):
        if bcrypt.checkpw(password=str.encode(password), hashed_password=str.encode(user.password_hash)):
            return True
        else:
            return False

    @classmethod
    def is_there_any_admin(cls):
        with client.context():
            admin = cls.query(cls.admin == True, cls.suspended == False, cls.deleted == False).get()

            if admin:
                return True
            else:
                return False

    @classmethod
    def generate_session_token(cls, user, request):
        with client.context():
            # generate session token and its hash
            token = secrets.token_hex()
            token_hash = bcrypt.hashpw(password=str.encode(token), salt=bcrypt.gensalt(12))

            # create a session
            session = Session(token_hash=token_hash, ip=request.remote_addr, platform=request.user_agent.platform,
                              browser=request.user_agent.browser, user_agent=request.user_agent.string,
                              expired=(datetime.datetime.now() + datetime.timedelta(days=30)))

            # store the session in the User model
            if not user.sessions:
                user.sessions = [session]
            else:
                user.sessions.append(session)

            user.put()

            return token
