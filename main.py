import csv
import trueskill
from player import Player

if __name__ == "__main__":
    # let's import our csv of players and their ratings
    players = []
    with open('TestData.csv') as f:
        data = csv.reader(f)
        for i in data:
            newplayer = Player(i[0], int(i[1]))
            players.append(newplayer)

    for i in players:
        print(i)
