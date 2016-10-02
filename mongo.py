from pymongo import MongoClient
from databaseConfig import address, password, user, databseName, collectionName


def mongo_connect():
    # The password goes here and needs to be filled in with the proper pass
    # We're keeping sensitive info out of github
    # This is the address that mongo is at
    # This is the name of the user of the db
    mongouri = "mongodb://{0}:{1}@{2}".format(user, password, address)
    client = MongoClient(mongouri)
    db = client[databseName]
    coll = db[collectionName]
    return coll
    # Here are some examples of how to use the class
    # cursor = coll.find()
    # coll.insert({"meow": "here it is"})
    # for doc in cursor:
    #     print("found one")
    #     print(doc)
