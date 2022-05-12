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
websocket_connections_dict= {}

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
  currentWebSocketConnection = None
  userFlag = 1
  actualUsername = ""
  while True:
      data = ws.receive()
      print("this is the type of the data before JSON loads", type(data))
      print("this is the data of the data", data)
      data = json.loads(data)
      print("this is the type of the data before JSON loads", type(data))
      if str(data).startswith("username"):
        data = str(data)
        splitData = data.split(":")

        actualUsername = splitData[1]

   # websocket connetion dict should be { "<simple_websocket.ws.Server object at 0x7f653c114e50>": "coolguy"
   #                                       "<simple_websocket.ws.Server object at 0x7fnfdjfdfnei>: "batman"}

      print("does data == closing? ", str(data)==str("closing"))
      if str(data) == str("closing"):
        # TODO: write a function that finds the username in the dictionary and sets the userIndex to something other than 1000 
        userFromDict = websocket_connections_dict[str(ws)]
        userFlag = 0
        # for users in range(len(websocket_connections)):
        #     print("this is the current list of websocket connections : ", websocket_connections[users])
        #     print("this is the current websocket connection", currentWebSocketConnection)
        #     print("do they equal each other? ", currentWebSocketConnection == websocket_connections[users])
        #     if websocket_connections[users] == currentWebSocketConnection:
        #       userIndex = users
      currentWebSocketConnection = str(ws)
      if str(ws) not in websocket_connections_dict.keys():
        # TODO: add the websocket connection:username key value pair to the dict
        print("THE WS CONNECTION IS NOT IN THE DICT")
        websocket_connections_dict[currentWebSocketConnection] = actualUsername
        print("THE WS CONNECTION IS NOw IN THE DICT")
      if actualUsername not in websocket_connections_dict.values():
        websocket_connections_dict[currentWebSocketConnection] = actualUsername
        
      print('this is the ws connection = ' ,ws)
      # if ws not in websocket_connections:
      #   websocket_connections.append(ws)        
      if userFlag == 0:
        # TODO: Means the user left the page and needs we need to remove them 
        del websocket_connections_dict[currentWebSocketConnection]
        #  websocket_connections.pop(userFlag)
 
      print("these are the current users after a client leaves the user tab", websocket_connections_dict)

        
      print("this is the data sent from functions.js websocket = ", data)
      print("\n")

      # I need to set the key of "websocket" of all the users I receive from null to True
      # the current ws object I receive is tied to a specific user who connected. 
      # I need to get the "id" element from each user on the users page to then match it
      # with the id from the 
      print("these are the current websocket connections: ", websocket_connections_dict)
      print("\n")
      """
      How can I match a websocket connection to specific user?
      We are going to need to add a current user to the users page so we can match the 
      """
      # ws.send(data)
  # when this while loop breaks then we know the user left the users tab and are no longer active
 