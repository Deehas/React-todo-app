import pytest
from flask import url_for
from core.auth.forms import RegistrationForm, LoginForm


def test_index_page_works(client, app_context):
    # Test index page
    index_url = url_for("index")
    response = client.get(index_url)
    assert response.status_code == 200
    data = response.data.decode("utf8").lower()
    start_text = "Let’s get started"
    assert start_text.lower() in data


def test_login_page_works(client, app_context):
    # Test login page
    login_url = url_for("auth.login")
    login_form = LoginForm()
    response = client.get(login_url)
    assert response.status_code == 200
    data = response.data.decode("utf8").lower()
    start_text = "Login"
    assert start_text.lower() in data
    assert login_form.email.name.lower() in data
    assert login_form.password.name.lower() in data
    assert login_form.remember_me.name.lower() in data


def test_register_page_works(client, app_context):
    # Test register page
    register_url = url_for("auth.register")
    register_form = RegistrationForm()
    response = client.get(register_url)
    assert response.status_code == 200
    data = response.data.decode("utf8").lower()
    start_text = "Register"
    assert start_text.lower() in data
    assert register_form.username.name.lower() in data
    assert register_form.email.name.lower() in data
    assert register_form.password.name.lower() in data
    assert register_form.password2.name.lower() in data

