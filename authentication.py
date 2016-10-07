from bottle import (request, redirect)
import functools
import hashlib
import mongo
from alerts import save_danger

'''	requiresLogin
Function wrapper to require a user to be logged in to access a certain page.
Accomplishes this by requiring the 'logged_in_as' cookie to be present,
which is only set when a user logs in successfully.
'''


def requires_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.get_cookie('current_user'):
            save_danger('You need to be logged in to do that!')
            redirect('/login/')
        else:
            return func(*args, **kwargs)
    return wrapper


def check_login(db, username, password):
    """
    Checks if the username and password the user entered to log in is correct
    :param mongodb db: mongo database connection object
    :param string username: username of player to authenticate
    :param string password: password of player to authenticate
    :return list: list of errors that occurred, if list is empty then the user
        was properly authenticated
    """
    errors = []
    # Encrypt the entered password
    e_password = hashlib.sha256(password.encode()).hexdigest()
    # Sanitize our input.
    player = mongo.get_player(db, username)
    if player is None:
        errors.append('Invalid username or password!')
    elif player['password'] != e_password:
        errors.append('Invalid username or password!')
    return errors
