from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models.todo import Todo, Category
from . import task
from .forms import TaskForm
from .. import db
from datetime import datetime
from flask_jwt_extended import (
    jwt_required,
)


@task.route("/delete_task", methods=["POST"])
@jwt_required()
def delete_task():
    # To delete a todo
    try:
        delete_task_id = request.json.get("task_id")
        # Deletes todo if checkbox is ticked
        if delete_task_id is not None:
            # Confirms actual todo with the ticked checkbox
            todo = Todo.query.filter_by(id=delete_task_id).first()
            if todo is None:
                return {"msg": "Please provide id of task to be deleted."}, 400

            db.session.delete(todo)
            db.session.commit()

        # To confirm if checkbox is ticked
        else:
            return {"msg": "Please provide id of task to be deleted."}, 400

    except Exception as e:
        db.session.rollback()
        return {"msg": "Task deletion failed, please try again."}, 400

    response = {
        "msg": "Task deleted successfully.",
    }
    return response, 200


@task.route("/get-todos/<user_id>", methods=["GET"])
@jwt_required()
def get_todos(user_id):
    todos = []
    # Query category table for categories linked to logged in user
    try:
        # Query todo table for todos linked to logged in user
        all_todos = Todo.query.filter_by(user_id=user_id).all()
        for todo in all_todos:
            todos.append(todo.to_dict())
    except Exception as e:
        return {"msg": "Failed to get todos."}, 400

    response = {
        "todos": todos,
    }
    return response, 200


@task.route("/get-categories", methods=["GET"])
@jwt_required()
def get_categories():
    categories = []
    # Query category table for categories linked to logged in user
    try:
        all_categories = Category.query.all()
        for category in all_categories:
            categories.append(category.to_dict())
    except Exception as e:
        return {"msg": "Failed to get categories."}, 400

    response = {
        "categories": categories,
    }
    return response, 200


@task.route("/create-task/<user_id>", methods=["GET", "POST"])
@jwt_required()
def create_task(user_id):
    title = request.json.get("title")
    date_string = request.json.get("date")
    time_string = request.json.get("time")
    selected_category_id = request.json.get("category_id")

    if title is None or title == "":
        return {"msg": "Title field is required"}, 400

    if selected_category_id is None or selected_category_id == "":
        return {"msg": "Category field is required"}, 400

    if date_string is None or date_string == "":
        return {"msg": "Date field is required"}, 400

    if time_string is None or time_string == "":
        return {"msg": "Time field is required"}, 400

    # Convert date string to date
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    # Convert time string to time
    time = datetime.strptime(time_string, "%H:%M").time()
    # To create a todo
    try:
        selected_category_id = selected_category_id
        category = Category.query.get(selected_category_id)
        todo = Todo(
            title=title,
            date=date,
            time=time,
            category=category.name,
            user_id=user_id,
        )
        db.session.add(todo)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return {"msg": "Task creation failed, please try again."}, 400

    response = {
        "msg": "Congratulations, you just added a new task",
        "todo": todo.to_dict(),
    }
    return response, 201
