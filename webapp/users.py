from flask import Blueprint, render_template,request, flash, session, blueprints
from webapp.database import add_message,list_messages


usersGiver = Blueprint("users", __name__)

@usersGiver.route('/users')
def home():
    return render_template("users.html", users = [])