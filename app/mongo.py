from pymongo import MongoClient

from config.databaseConfig import address, password, user, databse_name, player_coll, results_coll, tourny_coll


class DataBaseInfoException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        print(self.message)


def get_mongo_db():
    """
    Initializes a connection to mongo and returns the database object
    :return: database object to be used for mongo connections
    """
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
    """
    Returns all players in the players collection
    :param mongodb db: mongo database connection object
    :return: list of all players in the players collection
    """
    player_list = []
    for doc in db[player_coll].find():
        player_list.append(doc)
    return player_list


def get_player(db, username):
    """
    Given a username, returns a specific user in the players collection
    :param mongodb db: mongo database connection object
    :param username: username of player to be returned
    :return: returns the player that is found, and None if no player is found

    :raises DataBaseInfoException: raises exception if there is more than one
        user with the same username, this means there is a problem with the
        database/logic that needs to be fixed
    """
    result = None
    one_doc = False
    for doc in db[player_coll].find({"username": username}):
        if one_doc:
            err = "There should only be one name, please check database"
            raise DataBaseInfoException(err)
        result = doc
    return result


def insert_player(db, player_dict):
    """
    Inserts a new player document into the players collection
    :param mongodb db: mongo database connection object
    :param player_dict: information that needs to be inserted
    :return: None
    """
    db[player_coll].insert_one(player_dict)


def update_player(db, player_username, new_player):
    """
    Simple update line that replaces player with new_player
    :param mongodb db: mongo database connection object
    :param player_username: username of player to replace
    :param new_player: new player object to replace player
    :return: None
    """
    db[player_coll].replace_one(player_username, new_player)


def get_all_tournies(db):
    """
    Returns a list of all tournaments in the tournament collection
    :param mongodb db: mongo database connection object
    :return: list of tournaments in the tournament collection
    """
    tourny_list = []
    for doc in db[tourny_coll].find():
        tourny_list.append(doc)
    return tourny_list


def get_tourny(db, identifier):
    """
    Gets a specific tournament from the tournament collection
    :param mongodb db: mongo database connection object
    :param identifier: unique identifier for the tournament
    :return dict: returns dictionary result of tournament
    :raises DataBaseInfoException: Raises an exception if there is more than
        one document matching the query, if this occurs then there is an issue
        with the database or the logic behind it
    """
    result = None
    one_doc = False
    identifying_field = "date"
    for doc in db[tourny_coll].find({identifying_field: identifier}):
        if one_doc:
            err = "There should only be one tournament, please check database"
            raise DataBaseInfoException(err)
        result = doc
    return result


def get_all_results(db):
    """
    Gets all results in the results collection
    :param mongodb db: mongo database connection object
    :return list: returns a list of all results in the results collection
    """
    result_list = []
    for doc in db[results_coll].find():
        result_list.append(doc)
    return result_list


def get_result(db, key):
    """
    Gets a specific result from the result collection
    :param mongodb db: mongo database connection object
    :param key: key for finding a specific result in the results collection
    :return dict: returns dict result of query
    :raises DataBaseInfoException: Raises exception if there is more than one
        result, if this occurs then there is an issue with how the database is
        set up/the logic implementing this
    """
    result = None
    one_doc = False
    for doc in db[results_coll].find({"key": key}):
        if one_doc:
            err = "There should only be one result, please check database"
            raise DataBaseInfoException(err)
        result = doc
    return result

