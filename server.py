from beaker.middleware import SessionMiddleware
from bottle import (app, get, post, response, request, route, run, jinja2_view,
                    redirect, static_file)

from app import mongo
from app.alerts import load_alerts, save_danger, save_success
from app.authentication import check_login
from app.signup import form_validation, form_insertion
from app.users import retrieve_user_info, edit_user_profile, get_mains
from config.setup import melee_characters

db = mongo.get_mongo_db()

@route('/assets/<path:path>')
def static(path):
    return static_file(path, root='assets')

# @get('/')
# @jinja2_view('templates/home.html')
# def show_homepage():
#     sorted_players = ratings.sorted_ratings('Players.json')
#     return {'players': sorted_players}

# Main page.
@get('/')
@jinja2_view("templates/index.html")
@load_alerts
def index():
    # print(request.get_cookie('current_user'))
    if request.get_cookie('current_user'):
        return {'currentUser':request.get_cookie('current_user')}
    return {}


# Login page
@get('/login/')
@jinja2_view("templates/login.html")
@load_alerts
def show_login():
    if request.get_cookie('current_user'):
        redirect('/')
    return {}


@post('/login/')
def validate_login():
    login_form = request.forms
    errors = check_login(db, login_form['username'], login_form['password'])
    if errors:
        for i in errors:
            save_danger(i)
        redirect('/login/')
    # If user signed in successfully:
    # Grab their username, and sanitize it.
    username = login_form['username']
    # Create a session variable equal to their username:
    response.set_cookie("current_user", username, path='/')
    # Let them know they've been signed in successfully:
    save_success('Successfully logged in as {}'.format(username))
    # Redirect them back to the home page:
    redirect('/')


# Signup page
@get('/signup/')
@jinja2_view("templates/signup.html")
@load_alerts
def show_signup():
    if request.get_cookie('current_user'):
        return {'currentUser':request.get_cookie('current_user')}
    return {}


@post('/signup/')
def validate_signup():
    signup_form = request.forms
    errors = form_validation(db, signup_form)
    if errors:
        for i in errors:
            save_danger(i)
        redirect('/signup/')
    else:
        form_insertion(db, signup_form)
        save_success('Account created successfully!')
        redirect('/login/')


# Logout of the website.
@get('/logout/')
@load_alerts
def log_out():
    if request.get_cookie('current_user'):
        response.set_cookie('current_user', "", path='/')
        save_success('You have been successfully logged out.')
    redirect('/')


# Profile page
@get('/users/<username>/')
@jinja2_view("templates/profile.html")
@load_alerts
def show_profile(username):
    userInfo = retrieve_user_info(db, username)
    userInfo['username'] = username
    if request.get_cookie('current_user') == username:
        userInfo['ownsProfile'] = True
    if request.get_cookie('current_user'):
        userInfo['currentUser'] = request.get_cookie('current_user')
    userInfo['characters'] = melee_characters
    userInfo['charMains'] = get_mains(db, username)
    return userInfo


# Submitting a profile change
@post('/users/<username>/')
@load_alerts
def change_profile(username):
    if request.get_cookie('current_user'):
        errors = edit_user_profile(db, request.forms, username)
        if errors:
            for err in errors:
                save_danger(err)
                redirect('/users/{}/'.format(username))
        else:
            save_success('Profile changed successfully!')
            redirect('/users/{}/'.format(username))
    else:
        redirect('/users/{}/'.format(username))

sessionOptions = {
    'session.type': 'cookie',
    'session.validate_key': 'super-secret'
}
smash_rankings = app()
smash_rankings = SessionMiddleware(smash_rankings, sessionOptions)

# Run the server:
if __name__ == '__main__':
    run(app=smash_rankings, host='localhost', port=3000)
