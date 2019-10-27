from urllib.request import Request, urlopen
import pytest

from main import app
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_index_page(client):
    response = client.get('/')
    assert b'When you need TODO' in response.data


def test_login_get(client):
    response = client.get('/')
    assert b'Login' in response.data


def test_login_post_success(client):
    user = User.create(username="testman", password="test123")

    data = {"login-username": "testman", "login-password": "test123"}
    response = client.post('/login', data=data, follow_redirects=True)
    assert b'My tasks' in response.data


def test_login_post_fail(client):
    user = User.create(username="testman", password="test123")

    data = {"login-username": "testman", "login-password": "wrong12345"}  # WRONG PASSWORD!!!
    response = client.post('/login', data=data, follow_redirects=True)
    assert 403 == response.status_code


def test_first_admin_get(client):
    response = client.get('/first-admin')
    assert b'Admin registration' in response.data


def test_first_admin_post(client):
    # create the first user and admin
    data = {"first-admin-username": "testman", "first-admin-password": "test123", "first-admin-repeat": "test123"}
    response = client.post('/first-admin', data=data)
    assert b'Success' in response.data

    # find the user in the database, assert it exists
    testman = User.get_by_username(username="testman")
    assert testman is not None
    assert testman.admin is True
