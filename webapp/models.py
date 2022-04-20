from flask_login import LoginManager, UserMixin
from .database import mongo_client


login_manager = LoginManager()

"""
a Database model is essentially a blueprint for an object that will be stored in a database
"""

class User(UserMixin, mongo_client.db.Model):
    db= "hello"
