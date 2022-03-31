from webapp import mongo_client

users_collection = mongo_client.db.users_collection

users_id_collection = mongo_client.db.users_id_collection

# when ever we need a new id, we go into our file collection
# find one document, (that's all we will have in this collection)
def get_next_id():
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
    userDict = {"email":email, "fName":fName, "password":password}
    userDict["id"] = get_next_id()
    users_collection.insert_one(userDict)
    userDict.pop("_id")

def list_all():
    all_users = users_collection.find({}, {"_id": 0})
    print(list(all_users))
    return list(all_users)
