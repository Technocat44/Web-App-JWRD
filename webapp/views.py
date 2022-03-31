from flask import Blueprint, render_template

viewer = Blueprint('views', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@viewer.route('/')
def home():
    return render_template("home.html", user="James")