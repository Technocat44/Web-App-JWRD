from crypt import methods
import json
from flask import Blueprint, render_template,request, flash, session, blueprints
from webapp.database import get_all_users, fetch_messages, get_user_collection_via_auth_token
import time 
import json

usersGiver = Blueprint("users", __name__)

activeWebSocketConnections = []

@usersGiver.route("/ws")
def sock(ws):
  while True:
      activeWebSocketConnections.append()
      data = ws.receive()
      ws.send(data)
      # time.sleep(.10)

@usersGiver.route('/users')
def usersHandler():
    defaultPicture = 'https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png'
    users = get_all_users()
    toSend = []
    for user in users:
        # print(user)
        if user.get('login') == True:
            userSend = {}
            userSend['id'] = user['id']
            userSend['username'] = user['username']
            if user.get('profilePic') != None:
                userSend['profilePic'] = user['profilePic']
            else:
                userSend['profilePic'] = defaultPicture
            userSend['description'] = user.get('description', '')
            toSend.append(userSend)
    # print(1)
    # print(toSend)
    return render_template("users.html", users = toSend)

@usersGiver.route('/allUsers')
def allUsers():
    users = get_all_users() 
    toSend = []
    for user in users:
     #   print("what are the users", user)
        if user.get('login') == True:
            toSend.append(user)
    toSend = json.dumps(toSend)
    return toSend
  
# I need to write a function that identifies the current user by checking their auth token
# this function is used by the function.js file and returns a user
@usersGiver.route('/singleUser', methods = ["POST"])
def singleUser():
    auth_token = request.get_json()
    print("this is that data", auth_token)
    #auth_token = json.loads(data)
    print("the auth_token in /singleUser users.py", auth_token)
    userCollection = get_user_collection_via_auth_token(auth_token)
    user = userCollection["username"]
    user = json.dumps(user)
    return user

@usersGiver.route('/handleMessage', methods = ["POST"])
def handleMessageForm():
    return

@usersGiver.route('/fetchMessages', methods = ["POST"])
def fetchMessages():
    idToMessage = request.data
    dataToSend = {'id':session['id'], 'idToMessage': idToMessage}
    print(dataToSend)
    # print('abcd')
    return json.dumps({'id':session['id'], 'idToMessage': idToMessage})