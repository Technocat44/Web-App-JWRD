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
old_websocket_connections_dict= {}
username_websocket_connection_dict = {}
username_collection_dict = {}

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
  from webapp.database import fetch_messages, get_user_from_username, update_notifcation_to_True, update_websocket_to_False, update_wehsocket_to_True

  currentWebSocketConnection = None
  userFlag = 1
  actualUsername = ""
  while True:
      data = ws.receive()
      print("this is the type of the data before JSON loads", type(data))
      print("this is the data of the data", data)
      data = json.loads(data)
      print("this is the type of the data after JSON loads", type(data))

      ##### Handling a socket response with the clients username
      if str(data).startswith("username"):
        data = str(data)
        splitData = data.split(":")

        actualUsername = splitData[1]

   #username_websocket_connection_dict should be { "coolguy":"<simple_websocket.ws.Server object at 0x7f653c114e50>",
   #                                                "batman":"<simple_websocket.ws.Server object at 0x7fnfdjfdfnei>"}
      

      ###### Handling a socket response with the client id of the user who is to be notified that they recieved a message
      # the user received a message should be in form "update:<id number>"
      # TODO: Need to take the id, find it in the collections and update that users key of notification that they received a message
      usernameKey = ""
      if str(data)[:6] == str('update'):
        data = str(data)
        datasplit = data.split(":")
        wsid = int(datasplit[1])
        print("this is the usersId : ",wsid)
        print("this is the type of usersId :", type(wsid))
        for k,v in username_collection_dict.items():
          print("these are the keys in user_collection_dict", k, " type ", type(k))
          print("these are the values in users collection dict", v, " type ", type(v))
          if v['id'] == wsid:
            usernameKey = k
        # print('username updating: ', usernameKey)
        if usernameKey != "":
          connectionToSend = username_websocket_connection_dict.get(usernameKey, -1)
          print("init.py we're updating the users collection that they have a notification to True")
          update_notifcation_to_True(usernameKey)
          dict = username_collection_dict[usernameKey]
          dict["notifications"] = True
          if connectionToSend != -1:
            connectionToSend.send('fetch_messages')
      


      
      print("does data == closing? ", str(data)==str("closing"))
      ##### Handling a socket response when the user leaves the Users tab on the webpage, meaning they are no longer "active"]
      # this function sets the userFlag to 0 which is a signal and then if its 0 we remove them from the websocket connection dict
      if str(data) == str("closing"):
        # TODO: write a function that finds the username in the dictionary and sets the userIndex to something other than 1000 
        userFlag = 0


      ##### Handling a websocket response that contains all the current active userCollections
      # This is going to collect all the users who are logged in in a new dictionary.
      # if we have two dictionaries, one that contains the username:<websocket connection>
                                   # one that contains the username:userCollection
      if str(data).startswith("userCollection"):
        data = str(data)
        datasplit = data.split(":", 1)
        userColl = datasplit[1]
        print("the type of the userColl after splitting", type(userColl))
        print("userColl = ", userColl)
       # extracting the JSON str dictionary
        userColl = json.loads(userColl)
        userKey = userColl["username"]
        if userKey not in username_collection_dict.keys():
          username_collection_dict[userKey] = userColl


      
      if actualUsername != "":
        ### I need to store the currentWSConnetion as a string in order to see it properly
        username_websocket_connection_dict[actualUsername] = currentWebSocketConnection
        print("this is the actual username = ", actualUsername)
      
      
      print('this is the ws connection = ' ,ws)


      ## If the username is in the username_websocket_connection_dict then that means they are active and we can 
      # update the database and the username_collection_dict to reflect this.
      if actualUsername in username_websocket_connection_dict.keys() and actualUsername in username_collection_dict.keys():
        update_wehsocket_to_True(actualUsername)
        print("this is the type of the actual user name ", type(actualUsername))
        print("THESE ARE THE USER COLLECTION DICTS", username_collection_dict)
        dict = username_collection_dict[actualUsername]
        dict["websocketActive"] = True

        
      if userFlag == 0:
        # TODO: Means the user left the page and needs we need to remove them 
        del old_websocket_connections_dict[currentWebSocketConnection]
        del username_websocket_connection_dict[actualUsername]
        # take the actualUsername, and update the collection in the database
        print("setting the websocket connection to false")
        update_websocket_to_False(actualUsername)
        dict = username_collection_dict[actualUsername]
        dict["websocketActive"] = False

        print("these are the current users after a client leaves the user tab", username_websocket_connection_dict)

        
      print("this is the data sent from functions.js websocket = ", data)
      print("\n")

      # I need to set the key of "websocket" of all the users I receive from null to True
      # the current ws object I receive is tied to a specific user who connected. 
      # I need to get the "id" element from each user on the users page to then match it
      # with the id from the 
      print("these are the current websocket connections dictionary: ", username_websocket_connection_dict)
      print("these are all the collections from all the users that are logged in: ", username_collection_dict)

      print("\n")



      currentWebSocketConnection = ws

      ###### OLD CODE BUT LEAVE IT IN CASE WE NEED IT
      if ws not in old_websocket_connections_dict.keys():
        # TODO: add the websocket connection:username key value pair to the dict
        print("THE WS CONNECTION IS NOT IN THE DICT")
        old_websocket_connections_dict[currentWebSocketConnection] = actualUsername
        print("THE WS CONNECTION IS NOw IN THE DICT")
      if actualUsername not in old_websocket_connections_dict.values():
        old_websocket_connections_dict[currentWebSocketConnection] = actualUsername
        # this adds a username as a key and a websocket connection as a value
      """
      How can I match a websocket connection to specific user?
      We are going to need to add a current user to the users page so we can match the 
      """
      # ws.send(data)
  # when this while loop breaks then we know the user left the users tab and are no longer active
 