import pytest
from flask import url_for
from datetime import datetime
from core.models.todo import Todo


def test_create_task_fails_without_title(client, app_context, category1):
    # Test task creation without title
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "",
        "category": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "this field is required" in data


def test_create_task_fails_without_selecting_a_category(client, app_context, category1):
    # Test task creation without selecting a category
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Sell wares",
        "category": None,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "this field is required" in data


def test_create_task_fails_without_setting_date(client, app_context, category1):
    # Test task creation without settting date
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Call HR",
        "category": category1.id,
        "date": None,
        "time": current_time,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "this field is required" in data


def test_create_task_fails_without_setting_time(client, app_context, category1):
    # Test task creation without settting time
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "",
        "category": category1.id,
        "date": current_date,
        "time": None,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "this field is required" in data


def test_create_task_success(client, app_context, category1):
    # Test task creation
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Buy books",
        "category": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "congratulations, you just added a new task" in data


def test_delete_task_success(client, app_context, category1, test_db):
    # Test task deletion
    
    # Create new task
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Buy books",
        "category": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "congratulations, you just added a new task" in data

    # Get created task
    created_task = Todo.query.filter_by(title="Buy books").first()

    # Delete  task
    delete_task_url = url_for("task.delete_task")
    payload = {
        "checkedbox": created_task.id,
    }
    response = client.post(delete_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "task deleted successfully" in data


def test_delete_task_fails_without_selecting_a_todo(
    client, app_context, category1, test_db
):
    # Test task deletion

    # Create new task
    create_task_url = url_for("task.manage_task")

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Play ball",
        "category": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(create_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "congratulations, you just added a new task" in data

    # Get created task
    created_task = Todo.query.filter_by(title="Buy books").first()

    # Delete  task
    delete_task_url = url_for("task.delete_task")
    payload = {
        "checkedbox": None,
    }
    response = client.post(delete_task_url, data=payload, follow_redirects=True)
    data = response.data.decode("utf8").lower()
    assert "please check-box of task to be deleted" in data
