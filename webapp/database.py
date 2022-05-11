
from flask import request
from flask_pymongo import PyMongo
import certifi
import hashlib
from webapp.models import user_session

from webapp import auth

mongo_client = PyMongo(tlsCAFile=certifi.where())


"""
I set these collections up on Mongo Atlas first and then connected to them through mongo_client.
I want to keep all the database functions separate from the views so that is why I created the database.py file

The collections have to be inside the functions, because of the app factory structure, the db won't be 
initialized until inside of the routes. So in this case, we only call these functions when we enter routes

NOTES:
How to use find_one instead of find
https://stackoverflow.com/questions/28968660/how-to-convert-a-pymongo-cursor-cursor-into-a-dict
"""


#TODO: add user_session to the database, this should happen when a user successfully logs in
def add_user_session_to_db(user_name, login_key):
  logged_in_collection = mongo_client.db["logged_in"]
  if user_name == None:
    # if the user hasn't logged in their username will be None and they shouldn't be storing a session yet
    return False
  if login_key == False:
    return False
  logged_in_doc = {"username": user_name, "login": login_key}
  logged_in_collection.insert_one(logged_in_doc)
  return True

# when ever we need a new id, we go into our file collection
# find one document, (that's all we will have in this collection)
def get_next_id():
  users_id_collection = mongo_client.db["users_id_collection"]
  id_object = users_id_collection.find_one({}) # retrieve the doc
  if id_object: # if there is one in there, grab the last id, convert to int, increment by 1 
    next_id = int(id_object["last_id"]) + 1 
    # update the record using the set command
    users_id_collection.update_one({}, {"$set": {"last_id": next_id}})
    return next_id # then reutnr 
  else: # if it doesn't exist this will make the first id
    users_id_collection.insert_one({"last_id": 1})
    return 1

def get_all_users():
  users_collection = mongo_client.db["users_collection"]
  usersData = users_collection.find({}, {"_id":0, "password":0,"salt":0})
  return usersData

def set_user_login_to_true(username, bool):
  users_collection = mongo_client.db["users_collection"]
  users_collection.find_one_and_update({"username":username}, {"$set": {"login": bool}})

"""
   user_collection example =
  {"username": "jamesaqu", "email": "jamesaqu@buffalo.edu",  "password": "$2js7fng84n7ab7fb949",
   "id": Number, "auth_token": will be blank at sign up }
"""
def create_user_in_db(email, username, hashedpw, salt, login, profpic, websocketConn):
  users_collection = mongo_client.db["users_collection"]
  userDict = {"email":email, "username":username, "password":hashedpw,"salt":salt, "login":login, "profilePic": profpic,"description":"", "websocketActive": websocketConn}
  userDict["id"] = get_next_id()
  users_collection.insert_one(userDict)
  userDict.pop("_id")
  return userDict["id"]

def list_all():
  users_collection = mongo_client.db["users_collection"]
  all_users = users_collection.find({}, {"_id": 0})
  print(list(all_users))
  return list(all_users)

# this is not a security check, this only verifies if the user exist, and since usernames are unique only one will be 
# in the database. This function is only designed to verify if the username exists that is it.
def check_if_user_exist_on_signup(username) -> bool:
  users_collection = mongo_client.db["users_collection"]
  users = users_collection.find_one({"username":username}, {"username":1, "_id":0}) # this retrieves the user if they exist
  print("this is the user name we found in the database collection : ", users)
  if users: # if the query returned a username matching the sign up return True the username exist
    return True 
  else: # if the query does not return a username, return False
    return False

def retrieve_user(username) -> dict:
  users_collection = mongo_client.db["users_collection"]
  userFromDb = users_collection.find_one({"username":username}, {"_id":0}) # retrieve user and ignore _id tag
  if userFromDb:
    return userFromDb
  else:
    return False

def add_auth_token_to_users_collection(hash_auth_token, username):
  users_collection = mongo_client.db["users_collection"]
  print("/database::: addng auth token to user collection")
  print("/database::this is the user I am using to update auth_token", username)
  users_collection.find_one_and_update({"username":username["username"]},
                               { "$set" : {"auth_token":hash_auth_token} }) 

# THE UNIVERSAL FUNCTION
# get user_collection from a matching cookie
def get_user_collection_via_auth_token(auth_token):
  users_collection = mongo_client.db["users_collection"]
  hash_of_auth_token_cookie = hashlib.sha256(auth_token.encode()).hexdigest()
  print("/database hash of auth token cookie", hash_of_auth_token_cookie)
  userVerifiedFromDB = users_collection.find_one({"auth_token":hash_of_auth_token_cookie})
  return userVerifiedFromDB

def update_auth_token_to_None(username):
  users_collection = mongo_client.db["users_collection"]
  users_collection.find_one_and_update({"username":username["username"]}, {"$set": {"auth_token": None}} )
# this function should update a users login to false
def update_login_to_False(username):
  users_collection = mongo_client.db["users_collection"]
  new_values = {"$set": {"login": False}}
  print("/database, update login to false", username)
  print("/database this is the username", username["username"])
  users_collection.find_one_and_update({"username": username["username"] }, new_values )
  

  

def retrieve_hashed_auth_token_from_db(hash_auth_cookie):
  users_collection = mongo_client.db["users_collection"]
  authTokenFromDB = users_collection.find_one({"auth_token":hash_auth_cookie})

  if authTokenFromDB:
    return authTokenFromDB
  else:
    return False

def verify_auth_token(auth_token_cookie):
  if auth_token_cookie == -1:
    return False
  hash_of_auth_token_cookie = hashlib.sha256(auth_token_cookie.encode()).hexdigest()
  hashedAuthFromDB = retrieve_hashed_auth_token_from_db(hash_of_auth_token_cookie)
  if hashedAuthFromDB:
    return True
  return False
# def verify_auth_token(auth_token_cookie):
#     if auth_token_cookie == -1:
#         return render_template("home.html", user=None)
#     hash_of_auth_token_cookie = hashlib.sha256(auth_token_cookie.encode()).hexdigest()
#     hashedAuthFromDB = retrieve_hashed_auth_token_from_db(hash_of_auth_token_cookie)
#     if hashedAuthFromDB:
#         return render_template("home.html", user=hashedAuthFromDB["username"])
#     return render_template("home.html", user=None)

def find_one(email):
  oneUser = mongo_client.db["users_collection"].find_one({"email": email})
  print("this is in the db file, in find_one functionthe response is: ", oneUser)
  # if the id does not exist, oneUser will equal null / None
  return oneUser
  
def getImageFileID():
  imID = mongo_client.db["imageNum"]
  imID_ob = imID.find_one({})
  if imID_ob:
    next_id = int(imID_ob['last_id']) + 1
    imID.update_one({},{'$set' : {'last_id' : next_id}})
    return next_id
  else:
    imID.insert_one({'last_id': 1})
    return 1

def insertImages(imageID):
  photoPaths = mongo_client.db["paths"]
  photoData = {'path': 'image-' + str(imageID) + '.jpg'}
  photoPaths.insert_one(photoData)
  #mongo_client.db.drop_collection("paths")
  return True

def getPhotos():
  photoPaths = mongo_client.db["paths"]
  arr = []
  for paths in photoPaths.find():
      arr.append(paths['path'])
  return arr

def add_message(user1, user2, message):
  # find if a collection for these users exist
  temp = mongo_client.db["messages_collections"].find({"users": {"$all": [user1, user2]}})
  found = []
  message_collections = mongo_client.db["messages_collections"]
  for x in temp:
    found.append(x)
  print(found)
  if len(found) == 0:
    message_collections.insert_one({"users": [user1, user2], "messages":[{"user": user1, "message": message}]})
  else:
    query = {"users": {"$all": [user1, user2]}}
    appender = {"$push":{"messages": {"user": user1, "message": message}}}
    message_collections.update_one(query, appender)

def fetch_messages(id1, id2):
  col = mongo_client.db["messages_collections"]
  case1 = col.find_one({'id1': id1, 'id2':id2})
  case2 = col.find_one({'id1': id2, 'id2':id1})
  if case1:
    return case1['massages']
  elif case2:
    return case2['massages']
  else:
    col.insert_one({'id1': id1, 'id2': id2, 'messages': []})
    return []

def list_messages(user1, user2):
  messages = mongo_client.db['messages_collections'].find_one({"users": {"$all": [user1, user2]}})
  found = []
  if messages == None:
    return None
  for x in messages["messages"]:
    found.append(x)
  # print(found)
  if len(found) == 0:
    return []
  else:
    return found

def insertProfilePic(imageID,user):
  users_collection = mongo_client.db["users_collection"]
  #photoData = {'path': 'image-' + str(imageID) + '.jpg'}
  print(user['username'],flush = True)
  for users in users_collection.find():
    if users['username'] == user['username']:
      users_collection.update_one(users,{'$set' : { "profile_pic" : 'image-' + str(imageID) + '.jpg'}})
      print('switched',flush = True)
  #mongo_client.db.drop_collection("paths")
  return True

def insertDesc(desc,user):
  users_collection = mongo_client.db["users_collection"]
  print(user['username'],flush = True)
  for users in users_collection.find():
    if users['username'] == user['username']:
      users_collection.update_one(users,{'$set' : { "description" : desc}})
      print('switched',flush = True)
  #mongo_client.db.drop_collection("paths")
  return True


  # def getProfilePic(user):
  #   users_collection = mongo_client.db["users_collection"]
  #   for users in users_collection.find():
  #     if()