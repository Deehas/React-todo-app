import json
from flask import request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
)
from flask_login import login_user
from . import auth
from ..models.auth import User
from .. import db


@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@auth.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Check if username already in use
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return {"msg": "Username already in use."}, 400

    # Check if email already in use
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return {"msg": "Email already registered."}, 400

    try:
        user = User(username=username.lower(), email=email.lower())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return {"msg": "Registration failed, please try again."}, 401

    access_token = create_access_token(identity=email)
    response = {
        "access_token": access_token,
        "user": user.to_dict(),
        "msg": "Congratulations, you are now a registered user!",
    }
    return response, 200


@auth.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    remember_me = request.json.get("remember_me", None)
    try:
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return {
                "msg": "Login failed. Invalid email or password. Please try again."
            }, 401
        else:
            login_user(user, remember=remember_me)
            # next_page = request.args.get("next")
            # if not next_page or urlsplit(next_page).netloc != "":
            #     # else redirect to the home page
            #     next_page = url_for("home.homepage")

    except Exception as e:
        db.session.rollback()
        return {"msg": "Login failed. Please try again."}, 401

    access_token = create_access_token(identity=email)
    response = {
        "access_token": access_token,
        "user": user.to_dict(),
        "msg": "Welcome back! You have successfully logged in.",
    }
    return response, 200


@auth.route("/logout")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
