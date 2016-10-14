import hashlib
from app import mongo
from config.errors import UserNotExist

def update_cur_users(db):
    """
    Grabs all users currently in the system
    :param mongodb db:
    :return list: returns a list of all users in the system
    """
    users = []
    users_dict = mongo.get_all_players(db)
    for user in users_dict:
        users.append(user['username'])
    return users


def retrieve_user_info(db, username):
    """
    Grabs information about the user
    :param mongodb db: db object to connect to mongo
    :param string username: username of the current user
    :return dict: returns a dictionary including the user info
    """
    # Takes a username, and returns a dict with info related to that user.

    user_info = {}
    user = mongo.get_player(db, username)
    try:
        user_info['fname'] = user['fname']
        user_info['lname'] = user['lname']
        user_info['location'] = user['location']
        if 'ranking' in user:
            user_info['ranking'] = user['ranking']
        return user_info
    except TypeError:
        raise UserNotExist


def edit_user_profile(db, form, username):
    """
    This function is used to update a users profile after they have submitted
     the form online
    :param mongodb db: a mongo database object
    :param dict form: the form submitted by the user
    :param string username: username of the person who we are editing
    :return: returns a list of errors that occurred
    """
    errors = []
    fname = form['fname']
    lname = form['lname']
    location = form['location']
    new_main = form['add-main']
    old_pass = form['old-pass']
    new_pass = form['new-pass']
    confirm_pass = form['new-pass-confirm']
    del_main = ''
    player = mongo.get_player(db, username)
    # We will create a new player object and overwrite the old one
    new_player = {}
    # This new player will be a copy of the old one initially
    for key, value in player.items():
        new_player[key] = value

    if 'del-main' in form.keys():
        del_main = form['del-main']
    if fname:
        # Make sure name is valid
        if len(fname) > 30:
            errors.append('Names must be less than 30 characters!')
        # Modify the database
        else:
            new_player['fname'] = fname
    if lname:
        # Make sure name is valid
        if len(lname) > 30:
            errors.append('Names must be less than 30 characters!')
        # Modify the database
        else:
            new_player['lname'] = lname
    if location:
        # Make sure location is valid
        new_player['location'] = location

    if new_main:
        if new_main != "Select an Option":
            if len(new_player['mains']) > 4:
                errors.append("You can not have more than 5 main characters")
            already_main = False
            for main in new_player['mains']:
                if main == new_main:
                    already_main = True
            if already_main:
                err = 'You already have {} as a main character'.format(new_main)
                errors.append(err)
            else:
                new_player['mains'].append(new_main)

    if del_main:
        if del_main != "Nothing":
            is_main = False
            # Double checking to make sure that this is a main in the list
            for value in new_player['mains']:
                if value == del_main:
                    is_main = True
            if is_main:
                new_player['mains'].remove(del_main)
            pass

    if new_pass:
        if old_pass:
            if confirm_pass == new_pass:
                if len(new_pass) >= 6 or len(new_pass) <= 36:
                    # passwordCursor = conn.cursor()
                    old_pass = hashlib.sha256(old_pass.encode()).hexdigest()
                    new_pass = hashlib.sha256(new_pass.encode()).hexdigest()
                    if new_player['password'] == old_pass:
                        new_player['password'] = new_pass
                    else:
                        errors.append("Incorrect password")
                else:
                    err = 'New password must be between 6 and 32 characters!'
                    errors.append(err)
            else:
                err = 'Your confirmation does not match the new password!'
                errors.append(err)
        else:
            errors.append('You must enter your old password!')

    print(len(errors))
    if len(errors) == 0:
        mongo.update_player(db, {"username": player['username']}, new_player)
    return errors


def get_mains(db, username):
    """
    Gets the lsit of main characters for the specified username
    :param mongodb db: database connection
    :param string username: username for the user we want the mains of
    :return list: returns a list of all the main characters on this user
    """
    user = mongo.get_player(db, username)
    mains = []
    for main in user['mains']:
        mains.append(main)
    return mains
