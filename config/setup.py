# User, password, host, database

with open("config/MeleeCharacters.txt") as meleeFile:
    meleeCharacters = meleeFile.read()
    meleeCharacters = meleeCharacters.splitlines()

with open("config/Admins.txt") as adminFile:
    admins = adminFile.read()
    admins = admins.splitlines()
