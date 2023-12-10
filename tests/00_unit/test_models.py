from core.models.auth import User
from core.models.todo import Category
from core.models.todo import Todo
from datetime import datetime


def test_new_user_success():
    """
    WHEN a new User is created
    THEN check the username and email fields are defined correctly
    """
    user = User(username="Saheed10", email="saheed@gmail.com")
    assert user.username == "Saheed10"
    assert user.email == "saheed@gmail.com"


def test_new_user_failure():
    """
    WHEN a new User is created
    THEN check if the username and email fields are not defined correctly
    """
    user = User(username="Saka", email="saka@yahoo.com")
    assert user.username != "Saheed10"
    assert user.email != "saheed@gmail.com"


def test_category_success():
    """
    Test that category is successfully created
    """
    category = Category(id=12345, name="Saka")
    assert category.id == 12345
    assert category.name == "Saka"


def test_category_failure():
    """
    Test that category creation is unsuccessful
    """
    category = Category(id=17645, name="Kabir")
    assert category.id != 12345
    assert category.name != "Saka"


def test_create_todo_success():
    """
    Test that todo is successfully created
    """
    date = datetime.now()
    current_date = (date.strftime("%Y-%m-%d"),)
    current_time = (date.strftime("%H:%M:%S"),)

    todo = Todo(
        id=4568,
        title="Buy books",
        date=current_date,
        time=current_time,
        category="personal",
        user_id=1234,
    )
    assert todo.id == 4568
    assert todo.title == "Buy books"
    assert todo.date == current_date
    assert todo.time == current_time
    assert todo.category == "personal"
    assert todo.user_id == 1234

def test_create_todo_failure():
    """
    Test that todo creation is unsuccessful
    """
    date = datetime.now()
    current_date = (date.strftime("%Y-%m-%d"),)
    current_time = (date.strftime("%H:%M:%S"),)
    fake_date = "2000-12-24"
    fake_time = "08:06:12"

    todo = Todo(
        id=4596,
        title="Sell toys",
        date=date,
        time=current_time,
        category="other",
        user_id=2356,
    )
    assert todo.id != 4568
    assert todo.title != "Buy books"
    assert todo.date != fake_date
    assert todo.time != fake_time
    assert todo.category != "personal"
    assert todo.user_id != 1234

