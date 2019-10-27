from urllib.request import Request, urlopen

import pytest

from main import app
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    # create User model and log it in
    # login is required for all handlers in this file
    user = User.create(username="testman", password="test123")
    session_token = User.generate_session_token(user=user)
    client.set_cookie(server_name="localhost", key="ninja-todo-session", value=session_token)

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_profile_main(client):
    response = client.get('/profile')
    assert b'My profile' in response.data
