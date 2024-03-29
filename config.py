import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Config object for database connection and secret key
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "its-a-secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
