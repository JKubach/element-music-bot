import os
import sys
import configparser
import pylast

config = configparser.ConfigParser()
config.read('config.ini')

credentials = config['lastfm']
user = credentials['username']
passw = credentials['password']
api_key = credentials['api']
api_secret = credentials['api_secret']

try:
    API_KEY = os.environ["LASTFM_API_KEY"]
    API_SECRET = os.environ["LASTFM_API_SECRET"]
except KeyError:
    API_KEY = api_key
    API_SECRET = api_secret

try:
    lastfm_username = os.environ["LASTFM_USERNAME"]
    lastfm_password_hash = os.environ["LASTFM_PASSWORD_HASH"]
except KeyError:
    lastfm_username = user
    lastfm_password_hash = passw

lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=lastfm_username,
    password_hash=lastfm_password_hash,
)
