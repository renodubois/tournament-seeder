import json
import trueskill
from player import Player


if __name__ == '__main__':
    # temporary tournament file for test, will use command line later
    tournament_file = 'rolla_weekly_4.json'
    # let's import our json of players and their ratings
    players = []
    with open('players.json') as raw_data:
        user_data = json.load(raw_data)

    # Go through our users and turn them into Player objects
    for user in user_data:
        players.append(Player(user['tag'], user['rating']))

    print(players)

    # Grab a tournament file, read the results and update the players' ratings
    with open(tournament_file) as raw_data:
        tourney_data = json.load(raw_data)


    # Go through given tournament and update ratings
    for match in tourney_data:
        # Match the players to the 'p1' and 'p2' fields given in the json

        # Player 1 was the winner
        if match['result'] == 0:
            # Run TrueSkill

            # Update ratings on .json
        # Player 2 was the winner
        else:
            # Run TrueSkill

            # Update ratings on .json

