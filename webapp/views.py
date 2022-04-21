from flask import Blueprint, render_template, request, session
import hashlib
viewer = Blueprint('views', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@viewer.route('/')
def home():
    from webapp.database import retrieve_hashed_auth_token_from_db
    # want to change it to check the auth_token 
    auth_token_cookie = request.cookies.get("auth_token", -1)
    if auth_token_cookie == -1:
        return render_template("home.html", user=None)
    hash_of_auth_token_cookie = hashlib.sha256(auth_token_cookie.encode()).hexdigest()
    hashedAuthFromDB = retrieve_hashed_auth_token_from_db(hash_of_auth_token_cookie)
    if hashedAuthFromDB:
        return render_template("home.html", user=hashedAuthFromDB["username"])
    return render_template("home.html", user=None)