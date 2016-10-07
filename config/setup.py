# User, password, host, database

with open("MeleeCharacters.txt") as meleeFile:
    meleeCharacters = meleeFile.read()
    meleeCharacters = meleeCharacters.splitlines()

with open("Admins.txt") as adminFile:
    admins = adminFile.read()
    admins = admins.splitlines()
