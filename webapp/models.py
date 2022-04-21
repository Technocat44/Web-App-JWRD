# from flask_login import LoginManager, UserMixin

from webapp import auth
from .database import mongo_client


# login_manager = LoginManager()

"""
example: I can set a user up like this when a new client signs up

session_data = User(username)
session_data.set_authentication(True)
session_data.get_authentication   === True    ||      signals the user is logged in


"""

class Session():

    def __init__(self, username):
        self.username = username  # instance variable unique to each instance
        self.state = {"username":username} # each session will have its own state to key track of the session data

    def set_authentication(self, authenticated): 
        """
        :param authenticated: should be set to either True or False 

        """
        self.authenticated = authenticated
        self.state["authenticated"] = authenticated
    
    def get_authentication(self): # returns True if user is authenticated or False if user is not authenticated
        return self.authenticated
 
    def set_session_cookie(self, auth_cookie): 
        """
        :param auth_cookie: will be set once user signs-up. will be an unhashed auth token

        """
        self.auth_cookie = auth_cookie
        self.state["auth_cookie"] = auth_cookie

    def get_session_cookie(self): # returns the auth token 
        return self.auth_cookie

    def set_login(self, login):
        """
        :param login: the login should be either True if the user is logged in, or False if they are not logged in
                      should be set to False when a user logs out
        
        """
        self.login = login 
        self.state["login"] = login

    def get_login(self): # returns True if logged in, False if not.
        return self.login 
        
    def print_session_state(self):
        print("current user session: ", self.state)
