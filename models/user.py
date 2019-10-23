import bcrypt

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
    def is_there_any_admin(cls):
        with client.context():
            admin = cls.query(cls.admin == True, cls.suspended == False, cls.deleted == False).get()

            if admin:
                return True
            else:
                return False
