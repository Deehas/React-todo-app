from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from . import auth
from .forms import RegistrationForm, LoginForm
from ..models.auth import User
from .. import db
from werkzeug.urls import urlsplit


@auth.route("/register", methods=["GET", "POST"])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for("home.homepage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data.lower(), email=form.email.data.lower()
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you are now a registered user!", category="success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            flash("Registration failed, please try again.", category="danger")
            db.session.rollback()

    elif form.errors:
        flash(form.errors, category="danger")

    return render_template("register.html", title="Register", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user is None or not user.check_password(form.password.data):
                flash(
                    "Login failed. Invalid email or password. Please try again.",
                    category="danger",
                )
            else:
                # If next page parameter exist in url, redirect to the url
                # this means the user was redirected to the login page from the original route
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get("next")
                if not next_page or urlsplit(next_page).netloc != "":
                    # else redirect to the home page
                    next_page = url_for("home.homepage")

                flash(
                    "Welcome back! You have successfully logged in.", category="success"
                )
                return redirect(next_page)

        except Exception as e:
            flash("Login failed, please try again.", category="danger")
            db.session.rollback()
            
    elif form.errors:
        flash(form.errors, category="danger")

    return render_template("login.html", title="Sign In", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
