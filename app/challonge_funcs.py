import challonge
from config.challongeConfig import username, api_key

challonge.set_credentials(username, api_key)
domain = "rollasmashdev"

# tournament_url = "rollasmash-Rollatrash6"
#
# tournament = challonge.tournaments.show(tournament_url)
# print(tournament['id'])
# print(tournament['name'])
# print(tournament['started-at'])
#
# print(tournament)


# participants = challonge.participants.index(tournament['id'])
#
# print(len(participants))
# for participant in participants:
#     print(participant['name'])
#

def get_tournament(tournament_name):
    url = '{}-{}'.format(domain, tournament_name)
    return challonge.tournaments.show(url)


def get_participants(tournament_id):
    return challonge.participants.index(tournament_id)


def create_tournament(tournament_name):
    url = tournament_name
    return challonge.tournaments.create(tournament_name, url, private=True, subdomain=domain)


def add_participant(tournament_id, challonge_username):
    return challonge.participants.create(tournament_id, challonge_username, challonge_username=challonge_username)


def check_participation(tournament_name, challonge_username):
    tournament = get_tournament(tournament_name)
    users = challonge.participants.index(tournament['id'])
    for user in users:
        if user['username'] == challonge_username and not user['invitation-pending']:
                return True
    return False


def delete_tournament(tournament_name):
    url = '{}-{}'.format(domain, tournament_name)
    challonge.tournaments.destroy(url)
