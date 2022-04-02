from flask import request
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

def find_one():
  oneUser = mongo_client.db.users_collection.find_one({"userName":request.form['userName']}, {"_id":0})
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
