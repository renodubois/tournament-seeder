import json
import trueskill
from player import Player


def update_ratings(player_file, tournament_file):
    # temporary tournament file for test, will use command line later
    # let's import our json of players and their ratings
    players = []
    with open(player_file) as raw_data:
        user_data = json.load(raw_data)

    # Go through our users and turn them into Player objects
    for user in user_data:
        rating_float = float(user['Rating'])
        players.append(Player(user['Tag'], rating_float))


    # Grab a tournament file, read the results and update the players' ratings
    with open(tournament_file) as raw_data:
        tourney_data = json.load(raw_data)

    # Go through given tournament and update ratings
    for match in tourney_data:
        # Match the players to the 'p1' and 'p2' fields given in the json
        p1_index = 0
        p2_index = 0
        for i in range(0, len(players)):
            if match['p1'] == players[i].tag:
                p1_index = i
            elif match['p2'] == players[i].tag:
                p2_index = i
        # Player 1 was the winner
        if match['result'] == 0:
            # Run TrueSkill
            players[p1_index].rating, players[p2_index].rating = trueskill.rate_1vs1(players[p1_index].rating, players[p2_index].rating)
        # Player 1 was the winner
        else:
            # Run TrueSkill
            players[p2_index].rating, players[p1_index].rating = trueskill.rate_1vs1(players[p2_index].rating, players[p1_index].rating)
    # Iterate through players list, send data to .json
    json_players = []
    for player in players:
        json_players.append({'Rating':player.rating.mu, 'Tag':player.tag})
    with open(player_file, 'w') as file:
        json.dump(json_players, file, sort_keys=True)
