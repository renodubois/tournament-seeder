import json
import trueskill
from player import Player


if __name__ == '__main__':
    # temporary tournament file for test, will use command line later
    tournament_file = 'rolla_weekly_4.json'
    # let's import our json of players and their ratings
    players = []
    with open('Players.json') as raw_data:
        user_data = json.load(raw_data)

    # Go through our users and turn them into Player objects
    for user in user_data:
        players.append(Player(user['Tag'], float(user['Rating'])))

    print(players[0].rating)
    players[0].rating, players[1].rating = trueskill.rate_1vs1(players[0].rating, players[1].rating)
    print(players[1].rating)
    print(players[0].rating)

# Grab a tournament file, read the results and update the players' ratings
    with open(tournament_file) as raw_data:
        tourney_data = json.load(raw_data)


    # Go through given tournament and update ratings
    for match in tourney_data:
        # Match the players to the 'p1' and 'p2' fields given in the json
        p1_index = 0
        p2_index = 0
        for index, player in enumerate(player_data):
            if match['p1'] == player.tag:
                p1_index = index
            elif match['p2'] == player.tag:
                p2_index = index
        # Player 1 was the winner
        if match['result'] == 0:
            # Run TrueSkill
            players[p1_index], players[p2_index] = trueskill.rate_1vs1(players[p1_index].rating, players[p2_index].rating)
        # Player 2 was the winner
        else:
            # Run TrueSkill
            players[p2_index], players[p1_index] = trueskill.rate_1vs1(players[p2_index].rating, players[p1_index].rating)
    # Iterate through players list, send data to .json
