from flask import render_template
from core import app


@app.route("/")
def index():
    return render_template("index.html", title="ToDo Application")
