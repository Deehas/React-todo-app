import pytest
from flask import url_for


def test_register_user_fails_with_unequal_password(client, app_context):
    # Test register process with unequal password
    register_url = url_for("auth.register")
    payload = {
        "username": "kaz",
        "email": "alm3@gmail.com",
        "password": "kazonto",
        "password2": "lamb",
    }
    response = client.post(register_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "field must be equal to password." in data
    assert "register" in data


def test_register_user_fails_with_invalid_email(client, app_context):
    # Test register process with invalid email
    register_url = url_for("auth.register")
    payload = {
        "username": "kaz",
        "email": "sa24",
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "invalid email address." in data
    assert "register" in data


def test_register_user_works(client, app_context):
    # Test register process
    register_url = url_for("auth.register")
    payload = {
        "username": "kaz",
        "email": "kaz@gmail.com",
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "congratulations, you are now a registered user!" in data
    assert "login" in data


def test_register_user_fails_with_duplicate_details(client, app_context):
    # Test register process with duplicate details
    register_url = url_for("auth.register")
    payload = {
        "username": "kaz",
        "email": "kaz@gmail.com",
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "username already in use." in data
    assert "email already registered." in data
    assert "register" in data


def test_login_user_fails_with_invalid_email(client, app_context):
    # Test login process wiht invalid email
    login_url = url_for("auth.login")
    payload = {
        "email": "sa",
        "password": "dhiserio",
    }
    response = client.post(login_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "invalid email address" in data


def test_login_user_fails_with_wrong_password(client, app_context):
    # Test login process with wrong password
    login_url = url_for("auth.login")
    payload = {
        "email": "kaz@gmail.com",
        "password": "dhiserio",
    }
    response = client.post(login_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "login failed. invalid email or password. please try again." in data


def test_login_user_works(client, app_context):
    # Test login process
    login_url = url_for("auth.login")
    payload = {
        "email": "kaz@gmail.com",
        "password": "kazonto",
    }
    response = client.post(login_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "welcome back! you have successfully logged in." in data


