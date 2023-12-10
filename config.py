import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfiguration(Configuration):
    DEBUG = False
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "todo.db")


class TestingConfiguration(Configuration):
    DEBUG = True
    TESTING = True
    SERVER_NAME = "TESTSERVER.localdomain"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


app_config = {
    "test": TestingConfiguration,
    "development": DevelopmentConfiguration,
}
