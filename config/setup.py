# Process data for admins and Smash4 characters.

with open("config/Smash4Characters.txt") as char_file:
    smash4_characters = char_file.read()
    smash4_characters = smash4_characters.splitlines()

with open("config/Admins.txt") as adminFile:
    admins = adminFile.read()
    admins = admins.splitlines()
