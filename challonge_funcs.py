import challonge
username = "ren0ace"
api_key = "kJpqCrimzZ6niiGaDF3EzwDm0JLfTz4b5f85KaNu"
challonge.set_credentials(username, api_key)

tournament_url = "http://rollasmash.challonge.com/Rollatrash6"

tournament = challonge.tournaments.show(tournament_url)
print(tournament['id'])
print(tournament['name'])
print(tournament['started-at'])

print(tournament)


participants = challonge.participants.index(tournament['id'])

print(len(participants))

print(participants)
