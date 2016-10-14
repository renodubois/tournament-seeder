import challonge
import pprint
#from config.setup import (api_user, api_key)

api_user = "ren0ace"
api_key = "kJpqCrimzZ6niiGaDF3EzwDm0JLfTz4b5f85KaNu"

pp = pprint.PrettyPrinter()

challonge.set_credentials(api_user, api_key)

tournament_url = "rollasmash-Rollatrash6"

tournament = challonge.tournaments.show(tournament_url)
print(tournament['id'])
print(tournament['name'])
print(tournament['started-at'])

print(tournament)

pp.pprint(challonge.matches.index(tournament_url))

participants = challonge.participants.index(tournament['id'])

print(len(participants))

print(participants)
