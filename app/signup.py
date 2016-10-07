import hashlib
import app.mongo


def form_validation(db, form):
    """
    Validates that the user form provided follows all of the proper constraints
    :param mongodb db: mongo database connection object
    :param form: form submitted by the user with the information to check
    :return list: returns a list of errors, if the list is empty then the form
        is valid
    """
    # Import all of the form information into variables
    username = form['username']
    fname = form['fname']
    lname = form['lname']
    location = form['location']
    password = form['password']
    password_confirm = form['password-confirm']
    # Create list to hold all the errors
    error = []
    # if type(username) is str:
    if len(username) < 4 or len(username) > 20:
        error.append('Username must be between 4 and 20 characters!')
    # Check to make sure the username is unique
    if username_exists(db, username):
        error.append('Username must be unique!')
    if fname == '':
        error.append('First name field must be filled out!')
    if len(fname) > 30:
        error.append('Names must be less than 30 characters!')
    # else:
    #    error.append('Please input a proper first name')
    # if type(lname) is str:
    if lname == '':
        error.append('Last name field must be filled out!')
    if len(lname) > 30:
        error.append('Names must be less than 30 characters!')
    # else:
    #    error.append('Please input a proper last name')
    # if type(location) is str:
    if location == '':
        error.append('Location field must be filled out!')
    if len(password) < 6 or len(password) > 36:
        error.append('Password must be between 6 and 36 characters!')
    if password != password_confirm:
        error.append('Password does not match confirmation password!')

    return error


def form_insertion(db, form):
    """
    Inserts a player into the database based on a form
    :param mongodb db: mongo database connection object
    :param form: form submitted by the user to be inserted into the database
    :return: None
    """
    password = form['password']
    password = hashlib.sha256(password.encode()).hexdigest()
    user = {'username': form['username'],
            'password': password,
            'fname': form['fname'], 'lname': form['lname'],
            'location': form['location'],
            'mains': []}

    mongo.insert_player(db, user)


def username_exists(db, username):
    """
    Checks to see if the username already exists
    :param mongodb db: mongo database connection object
    :param username: username to check against
    :return boolean: returns True if the name already exists, False if otherwise
    """
    player = mongo.get_player(db, username)
    if player is None:
        return False
    return True
