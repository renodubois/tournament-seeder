from pymongo import MongoClient
from databaseConfig import address, password, user, databse_name, player_coll, results_coll, tourny_coll


class DataBaseInfoException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        print(self.message)


def get_mongo_db():
    # The password goes here and needs to be filled in with the proper pass
    # We're keeping sensitive info out of github
    # This is the address that mongo is at
    # This is the name of the user of the db
    mongouri = "mongodb://{0}:{1}@{2}".format(user, password, address)
    client = MongoClient(mongouri)
    db = client[databse_name]
    return db
    # Here are some examples of how to use the class
    # cursor = coll.find()
    # coll.insert({"meow": "here it is"})
    # for doc in cursor:
    #     print("found one")
    #     print(doc)


def get_all_players(db):
    player_list = []
    for doc in db[player_coll].find():
        player_list.append(doc)
    return player_list


def get_player(db, player_name):
    result = ""
    one_doc = False
    for doc in db[player_coll].find({"name": player_name}):
        if one_doc:
            err = "There should only be one name, please check database"
            raise DataBaseInfoException(err)
        result = doc
    return result


