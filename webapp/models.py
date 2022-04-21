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

class Session(object):

    def __init__(self, login):
        self.state = {"login":login} # each session will have its own state to key track of the session data
        self.login = login

    # def set_authentication(self, authenticated: bool): 
    #     """
    #     :param authenticated: should be set to either True or False 

    #     """
    #     self.authenticated = False
    #     self.state["authenticated"] = authenticated
    
    # def get_authentication(self):
    #     """
    #     :returns: True if user is authenticated or False if user is not authenticated
    #     """
    #     return self.authenticated
 
    def set_username(self, username: str):
        """
        :param username: when a user logs in we will set the username to what they signed up as
        """
        self.username = username
        self.state["username"] = username
    
    def get_username(self):
        return self.username

    def set_session_cookie(self, auth_cookie: str): 
        """
        :param auth_cookie: will be set once user signs-up. will be stored in state as an unhashed auth token

        """
        self.auth_cookie = auth_cookie
        self.state["auth_cookie"] = auth_cookie

    def get_session_cookie(self):
        """
        :returns: auth_token
        will be used to verify the user is authenticated.
        When a user with an auth token makes a request if the auth_token cookie they send matches the session auth token
        they have verified they are who they are!
        """
        return self.auth_cookie

    def set_login(self, login: bool):
        """
        :param login: the login should be either True if the user is logged in, or False if they are not logged in
                      should be set to False when a user logs out
        
        """
        self.login = login
        self.state["login"] = login

    def get_login(self): 
        """
        :returns: True if logged in, False if not.
        """
        return self.login 
        
    def print_session_state(self):
        print("current user session: ", self.state)

    def set_log_out(self):
        """
        wipes the state of the session 
        sets login to false
        """
        self.state = {}
        self.set_login(False)

user_session = Session(False)