from flask_pymongo import PyMongo
import certifi

mongo_client = PyMongo(tlsCAFile=certifi.where())

"""
I set these collections up on Mongo Atlas first and then connected to them through mongo_client.
I want to keep all the database functions separate from the views so that is why I created the database.py file

The collections have to be inside the functions, because of the app factory structure, the db won't be 
initialized until inside of the routes. So in this case, we only call these functions when we enter routes
"""

# when ever we need a new id, we go into our file collection
# find one document, (that's all we will have in this collection)
def get_next_id():
  users_id_collection = mongo_client.db.users_id_collection
  id_object = users_id_collection.find_one({}) # retrieve the doc
  if id_object: # if there is one in there, grab the last id, convert to int, increment by 1 
    next_id = int(id_object["last_id"]) + 1 
    # update the record using the set command
    users_id_collection.update_one({}, {"$set": {"last_id": next_id}})
    return next_id # then reutnr 
  else: # if it doesn't exist this will make the first id
    users_id_collection.insert_one({"last_id": 1})
    return 1

def createUser(email, fName, password):
    users_collection = mongo_client.db.users_collection
    userDict = {"email":email, "fName":fName, "password":password}
    userDict["id"] = get_next_id()
    users_collection.insert_one(userDict)
    userDict.pop("_id")

def list_all():
    users_collection = mongo_client.db.users_collection
    all_users = users_collection.find({}, {"_id": 0})
    print(list(all_users))
    return list(all_users)

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
    message_collections.find_one_and_update({"users": {"$all": [user1, user2]}}, )

def list_messages(user1, user2):
  messages = mongo_client.db['messages_collections'].find({"$or": [{'users': [user1, user2]},{'users': [user2,user1]}]})
  found = []
  for x in messages:
    found.append(x)
  if len(found) == 0:
    return []
  else:
    return x[0]