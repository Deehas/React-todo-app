import pytest
from flask import url_for
from datetime import datetime
from core.models.todo import Todo


def register_user(client, username="kaz", email="kaz@gmail.com"):
    # Test register process
    register_url = url_for("auth.register")
    payload = {
        "username": username,
        "email": email,
        "password": "kazonto",
        "password2": "kazonto",
    }
    response = client.post(register_url, json=payload)
    data = response.json
    assert response.status_code == 200
    assert "Congratulations, you are now a registered user!" in data["msg"]
    return data


def test_create_task_fails_without_title(client, app_context, category1, test_user):
    # Create new user
    new_user = register_user(client, "Bayo", "bayg@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Test task creation without title
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "",
        "category_id": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 400
    assert "Title field is required" in data["msg"]


def test_create_task_fails_without_selecting_a_category(
    client, app_context, category1, test_user
):
    # Create new user
    new_user = register_user(client, "Kamaldeen", "deen@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Test task creation without selecting a category
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Sell wares",
        "category_id": None,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 400
    assert "Category field is required" in data["msg"]


def test_create_task_fails_without_setting_date(
    client, app_context, category1, test_user
):
    # Create new user
    new_user = register_user(client, "Messi", "barca@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Test task creation without settting date
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Call HR",
        "category_id": category1.id,
        "date": "",
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 400
    assert "Date field is required" in data["msg"]


def test_create_task_fails_without_setting_time(
    client, app_context, category1, test_user
):
    # Create new user
    new_user = register_user(client, "Mbappe", "psg@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Test task creation without settting time
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Buy car",
        "category_id": category1.id,
        "date": current_date,
        "time": "",
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 400
    assert "Time field is required" in data["msg"]


def test_create_task_success(client, app_context, category1, test_user):
    # Create new user
    new_user = register_user(client, "Giveon", "soul@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Test task creation
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Buy books",
        "category_id": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 201
    assert "Congratulations, you just added a new task" in data["msg"]


def test_delete_task_success(client, app_context, category1, test_db, test_user):
    # Test task deletion

    # Create new user
    new_user = register_user(client, "Suleiman", "sule@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Create new task
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Buy books",
        "category_id": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 201
    assert "Congratulations, you just added a new task" in data["msg"]

    # Get created task
    task_id = data["todo"]["id"]
    created_task = Todo.query.filter_by(id=task_id).first()

    # Delete  task
    delete_task_url = url_for("task.delete_task")
    payload = {
        "task_id": created_task.id,
    }
    response = client.post(
        delete_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 200
    assert "Task deleted successfully." in data["msg"]


def test_delete_task_fails_without_todo_id(
    client, app_context, category1, test_db, test_user
):
    # Test task deletion

    # Create new user
    new_user = register_user(client, "Moshood", "rogue@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Create new task
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Play ball",
        "category_id": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 201
    assert "Congratulations, you just added a new task" in data["msg"]

    # Delete  task
    delete_task_url = url_for("task.delete_task")
    payload = {
        "task_id": 1324,
    }
    response = client.post(
        delete_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 400
    assert "Please provide id of task to be deleted." in data["msg"]


def test_get_all_user_todos_fails(client, app_context, category1, test_db, test_user):
    # Test task deletion

    # Create new user
    new_user = register_user(client, "Partey", "saka@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Create new task
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Eat sushi",
        "category_id": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 201
    assert "Congratulations, you just added a new task" in data["msg"]

    # Get  task
    get_task_url = url_for("task.get_todos", user_id=user_id)

    response = client.get(get_task_url)
    data = response.json
    assert response.status_code == 401


def test_get_all_user_todos_works(client, app_context, category1, test_db, test_user):
    # Test task deletion

    # Create new user
    new_user = register_user(client, "Thomas", "gabriel@gmail.com")
    # Create new task
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]
    create_task_url = url_for("task.create_task", user_id=user_id)

    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    current_time = date.strftime("%H:%M")

    payload = {
        "title": "Eat sushi",
        "category_id": category1.id,
        "date": current_date,
        "time": current_time,
    }
    response = client.post(
        create_task_url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json
    assert response.status_code == 201
    assert "Congratulations, you just added a new task" in data["msg"]

    # Get  task
    get_task_url = url_for("task.get_todos", user_id=user_id)

    response = client.get(
        get_task_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    data = response.json
    assert response.status_code == 200


def test_get_all_user_categories_fails(
    client, app_context, category1, test_db, test_user
):
    # Get categories
    get_categories_url = url_for("task.get_categories")

    response = client.get(get_categories_url)
    data = response.json
    assert response.status_code == 401


def test_get_all_user_categories_works(
    client, app_context, category1, test_db, test_user
):
    # Create new user
    new_user = register_user(client, "Ronaldo", "simeon@gmail.com")
    user_id = new_user["user"]["id"]
    access_token = new_user["access_token"]

    # Get categories
    get_task_url = url_for("task.get_todos", user_id=user_id)

    response = client.get(
        get_task_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    data = response.json
    assert response.status_code == 200
