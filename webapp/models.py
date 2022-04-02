from flask_login import LoginManager, UserMixin
from .database import mongo_client


login_manager = LoginManager()


class User(UserMixin, mongo_client.db.Model):
    db= "hello"
