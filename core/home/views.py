from flask import render_template, flash
from flask_login import login_required, current_user
from ..models.todo import Todo
from ..models.todo import Category
from . import home
from datetime import datetime
from flask_jwt_extended import (
    jwt_required,
)


@home.route("/")
@jwt_required()
def homepage():
    no_of_Task_ID_Business = 0
    no_of_Task_ID_Personal = 0
    no_of_Task_ID_Other = 0
    todos = []
    try:
        user = current_user
        # Query todo table for todos linked to logged in user
        all_todos = Todo.query.filter_by(author=user).order_by(Todo.date).all()
        for todo in all_todos:
            todos.append(todo.to_dict())
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
        return {"msg": "Loading homepage failed, please try again."}, 401

    response = {
        "todos": todos,
        "no_of_business_tasks": no_of_Task_ID_Business,
        "no_of_personal_tasks": no_of_Task_ID_Personal,
        "no_of_other_tasks": no_of_Task_ID_Other,
        "category_i_name": category1.name,
        "category_ii_name": category2.name,
        "category_iii_name": category3.name,
        "DateNow": now,
        "TimeNow": currentTime,
    }
    return response, 200
