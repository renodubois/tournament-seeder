from config.setup import (api_user, api_key)
import challonge


def convert_matches(match_data, tourney_url):
    """
    Converts data given to the Challonge API to a format easier to enter into our database.
    :param match_data: The dictionary given by the Challonge API containing match data for a tournament
    :param tourney_url: The ID of the tournament, needed to retrieve usernames.
    :return: A list of dicts, each one representing a match. The matches have 3 fields,
    player1 (string), player2 (string), and winner (string).
    """
    # Authenticating to the Challonge API
    challonge.set_credentials(api_user, api_key)
    # The list we're going to return.
    new_data = []
    # User Data from the Tournament
    user_data = challonge.participants.index(tourney_url)
    # Iterate through match_data, call get_challonge_name to get names of players.
    for match in match_data:
        # Temp object to use each iteration, grab player 1 and player 2 names
        temp = dict(player1=get_challonge_name(match['player1-id'], tourney_url, user_data),
                    player2=get_challonge_name(match['player2-id'], tourney_url, user_data),
                    winner="")
        # Determine the winner
        if match['scores-csv'][0] > match['scores-csv'][2]:
            temp['winner'] = "player1"
        else:
            temp['winner'] = "player2"
        # Append to new_data list
        new_data.append(temp)
    # Return our new data
    return new_data


def get_challonge_name(id, tourney_url, user_data):
    """
    Gets the Challonge username of a player ID for a given tournament.
    :param id: ID of the player we're trying to find.
    :param tourney_url: URL of the tournament that the player exists in.
    :param user_data: The object containing data on the participants of the tournament.
    :return: The user's Challonge username, as a string.
    """
    # Iterate through users
    for user in user_data:
        # If you find a match, return something
        if user['id'] == id:
            # If they have a challonge account, return that name
            if "challonge-username" in user:
                return user['challonge-username']
            # If not, return the name they used in the tournament.
            else:
                return user['name']