import os
import pytest
from core import create_app, db
from config import basedir
from core.models.todo import Category


os.environ["APP_SETTINGS"] = "test"
os.environ["FLASK_CONFIG"] = "test"
os.environ["FLASK_APP"] = os.path.join(basedir, "base.py")


# Create test app
@pytest.fixture(scope="session")
def test_app():
    app = create_app()
    yield app


# Create a test client using the Flask application configured for testing
@pytest.fixture(scope="session")
def client(test_app):
    client = test_app.test_client()
    return client


# Create test database
@pytest.fixture(scope="session", autouse=True)
def test_db(test_app):
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


# Create test app context
@pytest.fixture(scope="function")
def app_context(test_app):
    with test_app.test_request_context():
        yield


# create default categories
@pytest.fixture(scope="session", autouse=True)
def category1(test_db):
    category1 = Category(name="Business", id="1")

    test_db.session.add(category1)
    test_db.session.commit()

    yield category1
