from flask import Flask
from dotenv import load_dotenv
from flask_sock import Sock
import os

import json


load_dotenv(".flaskenv")
USERNAME = 'devUser'
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

print("U " ,USERNAME)
print("P "  ,PASSWORD)
print("D ", DATABASE) 

sock = Sock()

websocket_connections = []

def create_app():
    # __name__ is the name of the current Python module. 
    # The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
    app = Flask(__name__) 
    # SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during 
    # development, but it should be overridden with a random value when deploying.
    app.config['SECRET_KEY'] = 'dev'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["MONGO_URI"] = f"mongodb+srv://{USERNAME}:{PASSWORD}@clusterjwrd.49opx.mongodb.net/{DATABASE}?retryWrites=true&w=majority"
    from .database import mongo_client
    mongo_client.init_app(app)
   # from .models import login_manager
    # login_manager.init_app(app)
  
    sock.init_app(app)
    return app


@sock.route("/ws")
def socker(ws):
  while True:
      data = ws.receive()
      print("this is the data sent from functions.js websocket = ", data)
      print("\n")
      print('this is the ws connection = ' ,ws)

      # I need to set the key of "websocket" of all the users I receive from null to True
      # the current ws object I receive is tied to a specific user who connected. 
      # I need to get the "id" element from each user on the users page to then match it
      # with the id from the 

      """
      How can I match a websocket connection to specific user?
      We are going to need to add a current user to the users page so we can match the 
      """
      # ws.send(data)