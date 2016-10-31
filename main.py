from app import ratings

if __name__ == '__main__':
    ratings.update_ratings('Players.json', 'rolla_weekly_1.csv')
    ratings.update_ratings('Players.json', 'rolla_weekly_2.csv')
    ratings.update_ratings('Players.json', 'rolla_weekly_4.csv')

    print(ratings.sorted_ratings('Players.json'))
