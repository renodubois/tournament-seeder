# User, password, host, database

with open("config/MeleeCharacters.txt") as melee_file:
    melee_characters = melee_file.read()
    melee_characters = melee_characters.splitlines()

with open("config/Admins.txt") as admin_file:
    admins = admin_file.read()
    admins = admins.splitlines()
