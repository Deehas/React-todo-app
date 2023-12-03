from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models.todo import Todo, Category
from . import task
from .forms import TaskForm
from .. import db
from datetime import datetime


@task.route("/manage-task", methods=["GET", "POST"])
@login_required
def tasks():
    # Set check to none
    check = None
    user = current_user
    # Query todo table for todos linked to logged in user
    todos = Todo.query.filter_by(author=user)
    # Get current Date and Time
    date = datetime.now()
    # Format datetime to String
    now = date.strftime("%Y-%m-%d")

    form = TaskForm()
    # Query category table for selected category
    form.category.choices = [
        (category.id, category.name) for category in Category.query.all()
    ]

    if request.method == "POST":
        # To delete a todo
        if request.form.get("taskDelete") is not None:
            deleteTask = request.form.get("checkedbox")
            # Deletes todo if checkbox is ticked
            if deleteTask is not None:
                # Confirms actual todo with the ticked checkbox
                todo = Todo.query.filter_by(id=int(deleteTask)).one()
                db.session.delete(todo)
                db.session.commit()
                # Refreshes the page
                return redirect(url_for("task.tasks"))

            # To confirm if checkbox is ticked
            else:
                check = "Please check-box of task to be deleted"

        # To create a todo
        elif form.validate_on_submit():
            selected = form.category.data
            category = Category.query.get(selected)
            todo = Todo(
                title=form.title.data,
                date=form.date.data,
                time=form.time.data,
                category=category.name,
                author=user,
            )
            db.session.add(todo)
            db.session.commit()
            flash("Congratulations, you just added a new note")
            # Refreshes the page
            return redirect(url_for("task.tasks"))

    return render_template(
        "tasks.html",
        title="Create Tasks",
        form=form,
        todos=todos,
        DateNow=now,
        check=check,
    )
