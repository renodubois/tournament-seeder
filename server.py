import argparse
import socket
import sys
import ratings

from bottle import (app, Bottle, get, post, response, request, route, run, jinja2_view,
redirect, static_file)

@get('/')
@jinja2_view('templates/home.html')
def show_homepage():
    sorted_players = ratings.sorted_ratings('Players.json')
    return {'players':sorted_players}


smash_rankings = app()

# Run the server:
if __name__ == '__main__':
    run(app=smash_rankings, host='localhost', port=3000)
