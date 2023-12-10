from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models.todo import Todo, Category
from . import task
from .forms import TaskForm
from .. import db
from datetime import datetime


@task.route("/delete_task", methods=["POST"])
@login_required
def delete_task():
    # To delete a todo
    try:
        delete_task_id = request.form.get("checkedbox")
        # Deletes todo if checkbox is ticked
        if delete_task_id is not None:
            # Confirms actual todo with the ticked checkbox
            todo = Todo.query.filter_by(id=int(delete_task_id)).one()
            db.session.delete(todo)
            db.session.commit()
            flash("Task deleted successfully.", category="success")


        # To confirm if checkbox is ticked
        else:
            flash("Please check-box of task to be deleted.", category="warning")

    except Exception as e:
        flash("Task deletion failed, please try again.", category="danger")
        db.session.rollback()

    # Refreshes the page
    return redirect(url_for("task.manage_task"))


@task.route("/manage-task", methods=["GET", "POST"])
@login_required
def manage_task():
    user = current_user
    # Query todo table for todos linked to logged in user
    todos = Todo.query.filter_by(author=user).all()
    # Get current Date and Time
    date = datetime.now()
    # Format datetime to String
    now = date.strftime("%Y-%m-%d")
    # Format time to String
    time = date.strftime("%H:%M")

    form = TaskForm()
    # Query category table for selected category
    form.category.choices = [
        (category.id, category.name) for category in Category.query.all()
    ]

    if request.method == "POST":
        # To create a todo
        if form.validate_on_submit():
            try:
                selected_category_id = form.category.data
                category = Category.query.get(selected_category_id)
                todo = Todo(
                    title=form.title.data,
                    date=form.date.data,
                    time=form.time.data,
                    category=category.name,
                    author=user,
                )
                db.session.add(todo)
                db.session.commit()
                flash("Congratulations, you just added a new task", category="success")
                # Refreshes the page
                return redirect(url_for("task.manage_task"))

            except Exception as e:
                flash("Task creation failed, please try again.", category="danger")
                db.session.rollback()

        elif form.errors:
            flash(form.errors, category="danger")

    return render_template(
        "tasks.html",
        title="Manage Tasks",
        form=form,
        todos=todos,
        DateNow=now,
        TimeNow=time,
    )
