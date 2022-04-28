from flask import Blueprint, render_template, request
# from webapp.auth import user_session
import hashlib
viewer = Blueprint('views', __name__)

"""
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the 
incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. 
"""

@viewer.route('/')
def home():
    # I can use the session object or the auth token (verify_auth_token) request from the database.py
    from webapp.models import user_session
    print("this is the user_session", user_session)
    user_session.print_session_state()
    if user_session == None:
        return render_template("home.html", user=None)

    if user_session.get_login() == False:
        return render_template("home.html", user=None)
    else:
        return render_template("home.html", user=user_session.username)

    # return render_template("home.html", user=None)
    # # this checks the auth token cookie and verifies if it matches one from the database
    # # only a logged in user should have an auth token 
    # # want to change it to check the auth_token 
    # auth_token_cookie = request.cookies.get("auth_token", -1)
    # if auth_token_cookie == -1:
    #     return render_template("home.html", user=None)
    # hash_of_auth_token_cookie = hashlib.sha256(auth_token_cookie.encode()).hexdigest()
    # hashedAuthFromDB = retrieve_hashed_auth_token_from_db(hash_of_auth_token_cookie)
    # if hashedAuthFromDB:
    #     return render_template("home.html", user=hashedAuthFromDB["username"])
    # return render_template("home.html", user=None)