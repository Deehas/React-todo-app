from flask import render_template, flash
from flask_login import login_required, current_user
from ..models.todo import Todo
from ..models.todo import Category
from . import home
from datetime import datetime


@home.route("/home")
@login_required
def homepage():
    no_of_Task_ID_Business = 0
    no_of_Task_ID_Personal = 0
    no_of_Task_ID_Other = 0
    try:
        user = current_user
        # Query todo table for todos linked to logged in user
        todo = Todo.query.filter_by(author=user).order_by(Todo.date)
        # Get current Date and Time
        date = datetime.now()
        # Format date to String
        now = date.strftime("%Y-%m-%d")
        # Format time to String
        currentTime = date.strftime("%H:%M")

        # Retrieve categories with their IDs
        category1 = Category.query.get(1)
        category2 = Category.query.get(2)
        category3 = Category.query.get(3)

        # Get each task under each category
        Task_ID_Business = Todo.query.filter_by(category=category1.name, author=user)
        Task_ID_Personal = Todo.query.filter_by(category=category2.name, author=user)
        Task_ID_Other = Todo.query.filter_by(category=category3.name, author=user)

        # Get the number of task under each category
        no_of_Task_ID_Business = Task_ID_Business.count()
        no_of_Task_ID_Personal = Task_ID_Personal.count()
        no_of_Task_ID_Other = Task_ID_Other.count()

    except Exception as e:
        flash("Loading homepage failed, please try again.", category="danger")

    return render_template(
        "home.html",
        title="Home Page",
        todo=todo,
        no_of_business_tasks=no_of_Task_ID_Business,
        no_of_personal_tasks=no_of_Task_ID_Personal,
        no_of_other_tasks=no_of_Task_ID_Other,
        category_i=category1,
        category_ii=category2,
        category_iii=category3,
        DateNow=now,
        TimeNow=currentTime,
    )
