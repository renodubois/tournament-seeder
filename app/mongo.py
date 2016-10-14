import json
from pymongo import MongoClient
from config.databaseConfig import address, password, user, database_name, player_col, results_col, tourney_col


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
    mongouri = "mongodb://{0}:{1}@{2}".format(user, password, address)
    client = MongoClient(mongouri)
    db = client[database_name]
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
    for doc in db[player_col].find():
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
    for doc in db[player_col].find({"username": username}):
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
    db[player_col].insert_one(player_dict)


def update_player(db, player_username, new_player):
    """
    Simple update line that replaces player with new_player
    :param mongodb db: mongo database connection object
    :param player_username: username of player to replace
    :param new_player: new player object to replace player
    :return: None
    """
    player = {"username": player_username}
    db[player_col].replace_one(player, new_player)


def get_all_tournies(db):
    """
    Returns a list of all tournaments in the tournament collection
    :param mongodb db: mongo database connection object
    :return: list of tournaments in the tournament collection
    """
    tourny_list = []
    for doc in db[tourney_col].find():
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
    for doc in db[tourney_col].find({identifying_field: identifier}):
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
    for doc in db[results_col].find():
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
    for doc in db[results_col].find({"key": key}):
        if one_doc:
            err = "There should only be one result, please check database"
            raise DataBaseInfoException(err)
        result = doc
    return result


def check_for_previous(db, username, challonge_name):
    players = db[player_col].find({"challonge_name": challonge_name})
    if players.count() == 2:
        new_player = None
        challonge_player = None
        for doc in players:
            if doc['username']:
                if not new_player:
                    new_player = doc
                else:
                    return "two_users"
            else:
                challonge_player = doc
        for key, value in challonge_player:
            if value:
                new_player[key] = value
        return new_player
    return False
