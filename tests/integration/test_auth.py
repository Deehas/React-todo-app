import pytest
from flask import url_for


def test_register_user_works(client, app_context):
    # Test register process
    register_url = url_for("auth.register")
    payload = {
        "username": "kaz",
        "email": "kaz@gmail.com",
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, json=payload)
    data = response.json
    assert response.status_code == 200
    assert "Congratulations, you are now a registered user!" in data["msg"]


def test_register_user_fails_with_existing_username(client, app_context):
    # Test register process with duplicate details
    register_url = url_for("auth.register")
    payload = {
        "username": "kaz",
        "email": "kaz@yahoomail.com",
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, json=payload)
    data = response.json
    assert response.status_code == 400
    assert "Username already in use." in data["msg"]


def test_register_user_fails_with_existing_email(client, app_context):
    # Test register process with duplicate details
    register_url = url_for("auth.register")
    payload = {
        "username": "saka",
        "email": "kaz@gmail.com",
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, json=payload)
    data = response.json
    assert response.status_code == 400
    assert "Email already registered." in data["msg"]


def test_login_user_fails_with_wrong_password(client, app_context):
    # Test login process with wrong password
    login_url = url_for("auth.login")
    payload = {
        "email": "kaz@gmail.com",
        "password": "dhiserio",
    }
    response = client.post(login_url, json=payload)
    data = response.json
    assert response.status_code == 401
    assert "Login failed. Invalid email or password. Please try again." in data["msg"]


def test_login_user_works(client, app_context):
    # Test login process
    login_url = url_for("auth.login")
    payload = {
        "email": "kaz@gmail.com",
        "password": "kazonto",
    }
    response = client.post(login_url, json=payload)
    data = response.json
    assert response.status_code == 200
    assert "Welcome back! You have successfully logged in." in data["msg"]
